# ==========================================
# ENTRENADOR DE EMOCIONES (4 CLASES)
# Dataset: FER-2013 (Kaggle)
# Emociones: sad, happy, angry, neutral
# ==========================================
#!pip install tensorflow
import os
import zipfile
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt
import shutil

# --- CONFIGURACIÓN ---
NOMBRE_DEL_ZIP = "archive.zip"
IMG_SIZE = 48  # FER-2013 usa 48x48
BATCH_SIZE = 32
EPOCHS = 40

# MAPEO FER-2013 A 4 CLASES
# FER-2013 tiene: angry(0), disgust(1), fear(2), happy(3), sad(4), surprise(5), neutral(6)
FER_TO_4CLASS = {
    'angry': 'angry',
    'disgust': 'angry',  # Disgust se parece a angry
    'fear': 'sad',       # Fear se parece a sad
    'happy': 'happy',
    'sad': 'sad',
    'surprise': 'happy',  # Surprise la consideramos neutral
    'neutral': 'neutral'
}

def reorganizar_dataset(extract_path):
    """Reorganiza el dataset FER-2013 a solo 4 clases"""
    print("\n🔄 Reorganizando dataset a 4 clases...")

    train_dir = os.path.join(extract_path, 'train')
    test_dir = os.path.join(extract_path, 'test')

    # Crear nuevo directorio para dataset reorganizado
    nuevo_train = os.path.join(extract_path, 'train_4class')
    nuevo_test = os.path.join(extract_path, 'test_4class')

    # Crear carpetas para las 4 emociones
    for emocion in ['angry', 'happy', 'sad', 'neutral']:
        os.makedirs(os.path.join(nuevo_train, emocion), exist_ok=True)
        os.makedirs(os.path.join(nuevo_test, emocion), exist_ok=True)

    # Reorganizar train
    print("📁 Procesando imágenes de entrenamiento...")
    if os.path.exists(train_dir):
        reorganizar_carpeta(train_dir, nuevo_train)

    # Reorganizar test
    print("📁 Procesando imágenes de prueba...")
    if os.path.exists(test_dir):
        reorganizar_carpeta(test_dir, nuevo_test)

    return nuevo_train, nuevo_test

def reorganizar_carpeta(origen, destino):
    """Mueve archivos de 7 clases a 4 clases"""
    contador = {'angry': 0, 'happy': 0, 'sad': 0, 'neutral': 0}

    for carpeta_original in os.listdir(origen):
        ruta_carpeta = os.path.join(origen, carpeta_original)
        if not os.path.isdir(ruta_carpeta):
            continue

        # Mapear a nueva clase
        nueva_clase = FER_TO_4CLASS.get(carpeta_original.lower())
        if nueva_clase is None:
            continue

        # Copiar imágenes
        destino_clase = os.path.join(destino, nueva_clase)

        for archivo in os.listdir(ruta_carpeta):
            if archivo.endswith(('.jpg', '.png', '.jpeg')):
                origen_archivo = os.path.join(ruta_carpeta, archivo)
                # Renombrar para evitar duplicados
                nuevo_nombre = f"{carpeta_original}_{archivo}"
                destino_archivo = os.path.join(destino_clase, nuevo_nombre)

                shutil.copy2(origen_archivo, destino_archivo)
                contador[nueva_clase] += 1

    print(f"   ✓ Imágenes por clase: {contador}")

def crear_modelo(num_clases):
    """Crea modelo optimizado para imágenes en escala de grises"""
    print("\n🏗️ Construyendo modelo optimizado...")

    # Input en escala de grises (convertido a RGB para MobileNet)
    inputs = Input(shape=(IMG_SIZE, IMG_SIZE, 3))

    # MobileNetV2 preentrenado
    base_model = MobileNetV2(
        weights='imagenet',
        include_top=False,
        input_shape=(IMG_SIZE, IMG_SIZE, 3)
    )

    # Descongelar últimas capas para fine-tuning
    for layer in base_model.layers[:-30]:
        layer.trainable = False
    for layer in base_model.layers[-30:]:
        layer.trainable = True

    # Capas personalizadas
    x = base_model(inputs)
    x = GlobalAveragePooling2D()(x)
    x = Dense(256, activation='relu')(x)
    x = Dropout(0.5)(x)
    x = Dense(128, activation='relu')(x)
    x = Dropout(0.4)(x)
    outputs = Dense(num_clases, activation='softmax')(x)

    model = Model(inputs=inputs, outputs=outputs)

    model.compile(
        optimizer=Adam(learning_rate=0.0001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    return model

def sistema_principal():
    print("="*60)
    print("🚀 ENTRENADOR DE EMOCIONES - 4 CLASES")
    print("="*60)

    # 1. VERIFICAR ARCHIVO
    if not os.path.exists(NOMBRE_DEL_ZIP):
        print(f"❌ ERROR: No encuentro '{NOMBRE_DEL_ZIP}'")
        print("👉 Descarga FER-2013 de Kaggle y renómbralo a 'archive.zip'")
        return

    # 2. DESCOMPRIMIR
    print("\n📦 Descomprimiendo dataset...")
    extract_path = "./dataset_fer2013"
    if not os.path.exists(extract_path):
        with zipfile.ZipFile(NOMBRE_DEL_ZIP, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

    # 3. REORGANIZAR A 4 CLASES
    train_dir, test_dir = reorganizar_dataset(extract_path)

    # 4. VERIFICAR ESTRUCTURA
    print(f"\n📂 Dataset reorganizado en: {train_dir}")

    # 5. GENERADORES DE DATOS
    print("\n⚙️ Preparando generadores de imágenes...")

    # Generador de entrenamiento con aumento de datos
    train_datagen = ImageDataGenerator(
        rescale=1./255,
        rotation_range=15,
        width_shift_range=0.1,
        height_shift_range=0.1,
        zoom_range=0.1,
        horizontal_flip=True,
        validation_split=0.2
    )

    # Generador de prueba (solo normalización)
    test_datagen = ImageDataGenerator(rescale=1./255)

    train_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='rgb',  # Convertir a RGB para MobileNet
        class_mode='categorical',
        subset='training',
        shuffle=True
    )

    validation_generator = train_datagen.flow_from_directory(
        train_dir,
        target_size=(IMG_SIZE, IMG_SIZE),
        batch_size=BATCH_SIZE,
        color_mode='rgb',
        class_mode='categorical',
        subset='validation'
    )

    # 6. VERIFICAR CLASES
    emociones = list(train_generator.class_indices.keys())
    print(f"\n🧠 Clases detectadas: {emociones}")
    print(f"📊 Total imágenes entrenamiento: {train_generator.samples}")
    print(f"📊 Total imágenes validación: {validation_generator.samples}")

    if len(emociones) != 4:
        print(f"⚠️ ADVERTENCIA: Se esperaban 4 clases, se encontraron {len(emociones)}")

    # 7. CREAR MODELO
    model = crear_modelo(len(emociones))

    print("\n📋 Resumen del modelo:")
    model.summary()

    # 8. CALLBACKS
    callbacks = [
        EarlyStopping(
            monitor='val_accuracy',
            patience=5,
            restore_best_weights=True,
            verbose=1
        ),
        ReduceLROnPlateau(
            monitor='val_loss',
            factor=0.5,
            patience=3,
            min_lr=1e-7,
            verbose=1
        )
    ]

    # 9. ENTRENAR
    print(f"\n🏋️‍♀️ Iniciando entrenamiento ({EPOCHS} épocas)...")
    print("⏳ Esto puede tomar varios minutos...\n")

    history = model.fit(
        train_generator,
        validation_data=validation_generator,
        epochs=EPOCHS,
        callbacks=callbacks,
        verbose=1
    )

    # 10. RESULTADOS
    print("\n" + "="*60)
    print("🏆 ENTRENAMIENTO COMPLETADO")
    print("="*60)

    train_acc = history.history['accuracy'][-1] * 100
    val_acc = history.history['val_accuracy'][-1] * 100

    print(f"📈 Precisión Entrenamiento: {train_acc:.2f}%")
    print(f"📈 Precisión Validación: {val_acc:.2f}%")

    # 11. GUARDAR MODELO
    nombre_modelo = 'detector_emociones_4clases.h5'
    model.save(nombre_modelo)
    print(f"\n💾 Modelo guardado: {nombre_modelo}")
    print("✅ ¡Listo para usar en el detector en tiempo real!")

    # 12. GRÁFICAS
    print("\n📊 Generando gráficas de entrenamiento...")
    plt.figure(figsize=(12, 4))

    # Precisión
    plt.subplot(1, 2, 1)
    plt.plot(history.history['accuracy'], label='Train')
    plt.plot(history.history['val_accuracy'], label='Validation')
    plt.title('Precisión del Modelo')
    plt.xlabel('Época')
    plt.ylabel('Precisión')
    plt.legend()
    plt.grid(True)

    # Pérdida
    plt.subplot(1, 2, 2)
    plt.plot(history.history['loss'], label='Train')
    plt.plot(history.history['val_loss'], label='Validation')
    plt.title('Pérdida del Modelo')
    plt.xlabel('Época')
    plt.ylabel('Pérdida')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig('training_history.png')
    print("📊 Gráficas guardadas: training_history.png")

    print("\n" + "="*60)
    print("✨ PROCESO FINALIZADO")
    print("="*60)

if __name__ == "__main__":
    sistema_principal()
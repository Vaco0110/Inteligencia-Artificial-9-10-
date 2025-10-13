// Manejar envío del formulario
document.addEventListener('DOMContentLoaded', function() {
    const recommendationForm = document.getElementById('recommendationForm');
    if (recommendationForm) {
        recommendationForm.addEventListener('submit', function(e) {
            e.preventDefault();
            generarRecomendaciones();
        });
    }

    // Generar recomendaciones al cargar la página
    generarRecomendaciones();
});

function generarRecomendaciones() {
    const num_recomendaciones = document.getElementById('num_recomendaciones').value;
    const pelicula = document.getElementById('pelicula').value;

    // Mostrar loading
    const loadingElement = document.getElementById('loadingRecomendaciones');
    const resultadosElement = document.getElementById('resultadosRecomendaciones');
    
    if (loadingElement) loadingElement.style.display = 'block';
    if (resultadosElement) resultadosElement.innerHTML = '';

    fetch('/recomendar', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            num_recomendaciones: parseInt(num_recomendaciones),
            pelicula: pelicula
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error en la respuesta del servidor');
        }
        return response.json();
    })
    .then(data => {
        if (loadingElement) loadingElement.style.display = 'none';
        
        if (data.success) {
            mostrarResultados(data.recomendaciones, pelicula);
        } else {
            mostrarError(data.error || 'Error desconocido');
        }
    })
    .catch(error => {
        if (loadingElement) loadingElement.style.display = 'none';
        mostrarError('Error de conexión: ' + error.message);
    });
}

function mostrarResultados(recomendaciones, peliculaBase) {
    const resultadosElement = document.getElementById('resultadosRecomendaciones');
    if (!resultadosElement) return;

    let html = `
        <h5 class="mb-4">
            Películas similares a: 
            <span class="text-primary">"${peliculaBase}"</span>
        </h5>
    `;
    
    if (!recomendaciones || recomendaciones.length === 0) {
        html += `
            <div class="alert alert-warning fade-in">
                <i class="fas fa-exclamation-triangle me-2"></i>
                No se encontraron recomendaciones para esta película.
            </div>
        `;
    } else if (recomendaciones.length === 1 && recomendaciones[0].title === "Error") {
        html += `
            <div class="alert alert-danger fade-in">
                <i class="fas fa-times-circle me-2"></i>
                ${recomendaciones[0].genres}
            </div>
        `;
    } else {
        html += `
            <div class="table-responsive fade-in">
                <table class="table table-hover">
                    <thead>
                        <tr>
                            <th>Película</th>
                            <th>Géneros</th>
                            <th>Similitud</th>
                        </tr>
                    </thead>
                    <tbody>
        `;
        
        recomendaciones.forEach(item => {
            const score = item.score ? (item.score * 100).toFixed(1) + '%' : 'N/A';
            const badgeColor = getBadgeColor(item.score);
            
            html += `
                <tr class="fade-in">
                    <td>
                        <strong>${escapeHtml(item.title)}</strong>
                    </td>
                    <td>${escapeHtml(item.genres)}</td>
                    <td>
                        <span class="badge ${badgeColor}">
                            ${score}
                        </span>
                    </td>
                </tr>
            `;
        });
        
        html += `
                    </tbody>
                </table>
            </div>
            <div class="mt-3 text-muted small">
                <i class="fas fa-info-circle me-1"></i>
                Mostrando ${recomendaciones.length} recomendaciones
            </div>
        `;
    }
    
    resultadosElement.innerHTML = html;
}

function mostrarError(mensaje) {
    const resultadosElement = document.getElementById('resultadosRecomendaciones');
    if (resultadosElement) {
        resultadosElement.innerHTML = `
            <div class="alert alert-danger fade-in">
                <i class="fas fa-times-circle me-2"></i>
                ${escapeHtml(mensaje)}
            </div>
        `;
    }
}

function getBadgeColor(score) {
    if (!score) return 'bg-secondary';
    if (score > 0.8) return 'bg-success';
    if (score > 0.6) return 'bg-primary';
    if (score > 0.4) return 'bg-warning';
    return 'bg-secondary';
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
        .toString()
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}

// Manejar cambios en los campos del formulario
document.addEventListener('DOMContentLoaded', function() {
    const peliculaSelect = document.getElementById('pelicula');
    const numRecomendaciones = document.getElementById('num_recomendaciones');
    
    if (peliculaSelect) {
        peliculaSelect.addEventListener('change', function() {
            // Opcional: generar recomendaciones automáticamente al cambiar película
            // generarRecomendaciones();
        });
    }
    
    if (numRecomendaciones) {
        numRecomendaciones.addEventListener('change', function() {
            // Validar que esté dentro del rango permitido
            const value = parseInt(this.value);
            if (value < 1) this.value = 1;
            if (value > 20) this.value = 20;
        });
    }
});
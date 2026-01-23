// Main application JavaScript

// API Configuration
const API_BASE_URL = window.location.origin; // Uses current origin (http://localhost:8080)

let selectedImage = null;
let currentAnalysis = null;

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    const imageInput = document.getElementById('image-input');
    const uploadArea = document.getElementById('upload-area');
    const analyzeBtn = document.getElementById('analyze-btn');

    // Image selection
    imageInput.addEventListener('change', handleImageSelect);

    // Drag and drop
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleImageFile(files[0]);
        }
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeInstallation);
}

function handleImageSelect(e) {
    const file = e.target.files[0];
    if (file) {
        handleImageFile(file);
    }
}

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
        alert('Por favor selecciona un archivo de imagen');
        return;
    }

    selectedImage = file;

    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        const preview = document.getElementById('image-preview');
        const previewImg = document.getElementById('preview-img');
        const placeholder = document.querySelector('.upload-placeholder');

        previewImg.src = e.target.result;
        preview.style.display = 'block';
        placeholder.style.display = 'none';

        // Enable analyze button
        document.getElementById('analyze-btn').disabled = false;
    };
    reader.readAsDataURL(file);
}

async function analyzeInstallation() {
    if (!selectedImage) {
        alert('Por favor selecciona una imagen primero');
        return;
    }

    const installationType = document.getElementById('installation-type').value;
    const resultsSection = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const analysisResults = document.getElementById('analysis-results');

    // Show results section and loading
    resultsSection.style.display = 'block';
    loading.style.display = 'block';
    analysisResults.style.display = 'none';

    // Scroll to results
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    try {
        // Simulate progress steps
        await updateStep(1, '✓ Imagen recibida');
        await sleep(500);

        await updateStep(2, '⏳ Analizando elementos visuales...');

        // Send to server
        const formData = new FormData();
        formData.append('image', selectedImage);
        formData.append('installation_type', installationType);

        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || `Error del servidor (${response.status})`);
        }

        await updateStep(2, '✓ Análisis visual completado');
        await updateStep(3, '⏳ Consultando normativa...');
        await sleep(1000);

        await updateStep(3, '✓ Verificación normativa completada');
        await updateStep(4, '⏳ Generando dictamen...');
        await sleep(500);

        await updateStep(4, '✓ Dictamen generado');

        // Store analysis
        currentAnalysis = data.analysis;

        // Display results
        displayResults(data.analysis);

        // Hide loading, show results
        loading.style.display = 'none';
        analysisResults.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
        alert(`Error en el análisis: ${error.message}`);
        loading.style.display = 'none';
    }
}

function displayResults(analysis) {
    // Classification
    const classification = analysis.classification;
    const statusBadge = document.getElementById('classification-status');
    const classificationText = document.getElementById('classification-text');

    statusBadge.textContent = classification.status;
    statusBadge.className = 'status-badge ' + classification.status.toLowerCase().replace(/ /g, '-');
    classificationText.textContent = classification.justification;

    // Summary
    const summaryContent = document.getElementById('summary-content');
    summaryContent.innerHTML = `<pre>${analysis.summary}</pre>`;

    // Conformities
    const conformitiesTab = document.getElementById('conformities-tab');
    const conformities = analysis.vision_analysis.conformities || [];

    if (conformities.length > 0) {
        conformitiesTab.innerHTML = '<ul>' +
            conformities.map(c => `<li>✓ ${c}</li>`).join('') +
            '</ul>';
    } else {
        conformitiesTab.innerHTML = '<p>No se registraron conformidades específicas.</p>';
    }

    // Non-conformities
    const nonConformitiesTab = document.getElementById('non-conformities-tab');
    const nonConformities = analysis.verified_non_conformities || [];

    if (nonConformities.length > 0) {
        nonConformitiesTab.innerHTML = '<ul>' +
            nonConformities.map(nc => {
                const article = nc.article ? ` (Art. ${nc.article})` : '';
                const severity = nc.severity || 'medium';
                const icon = severity === 'high' ? '🔴' : severity === 'medium' ? '🟡' : '🟢';
                return `<li>${icon} ${nc.description}${article}</li>`;
            }).join('') +
            '</ul>';
    } else {
        nonConformitiesTab.innerHTML = '<p>No se detectaron no conformidades.</p>';
    }

    // Observations
    const observationsTab = document.getElementById('observations-tab');
    const observations = analysis.vision_analysis.observations || '';

    if (observations) {
        observationsTab.innerHTML = `<p>${observations}</p>`;
    } else {
        observationsTab.innerHTML = '<p>Sin observaciones adicionales.</p>';
    }

    // Acciones Sugeridas (from acciones_sugeridas or recommendations)
    const actionsTab = document.getElementById('actions-tab');
    const actions = analysis.vision_analysis.acciones_sugeridas || analysis.vision_analysis.recommendations || [];

    if (actions && actions.length > 0) {
        actionsTab.innerHTML = '<ul>' +
            actions.map(action => `<li>• ${action}</li>`).join('') +
            '</ul>';
    } else {
        // If no actions list, try to show dictamen
        const dictamen = analysis.vision_analysis.dictamen || '';
        if (dictamen) {
            actionsTab.innerHTML = `<p>${dictamen}</p>`;
        } else {
            actionsTab.innerHTML = '<p>No se generaron acciones sugeridas específicas.</p>';
        }
    }

    // Observaciones Adicionales (from observaciones_adicionales or risks)
    const additionalTab = document.getElementById('additional-tab');
    const additionalObs = analysis.vision_analysis.observaciones_adicionales || '';
    const risks = analysis.vision_analysis.risks || [];

    if (additionalObs) {
        additionalTab.innerHTML = `<p>${additionalObs}</p>`;
    } else if (risks && risks.length > 0) {
        additionalTab.innerHTML = '<ul>' +
            risks.map(risk => `<li>⚠️ ${risk}</li>`).join('') +
            '</ul>';
    } else {
        additionalTab.innerHTML = '<p>No se identificaron observaciones adicionales.</p>';
    }
}

function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    // Show selected tab
    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

async function downloadDictamen() {
    if (!currentAnalysis) {
        alert('No hay análisis disponible');
        return;
    }

    try {
        // Get inspector name
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Tu Nombre ]';

        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis: currentAnalysis,
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString('es-MX'),
                    inspector_name: inspectorName
                }
            })
        });

        const data = await response.json();

        if (data.success) {
            // Download file
            window.location.href = `/api/download/${data.filename}`;
        } else {
            alert('Error generando dictamen: ' + data.error);
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Error al generar dictamen');
    }
}

async function downloadDictamenWord() {
    if (!currentAnalysis) {
        alert('No hay análisis disponible');
        return;
    }

    try {
        // Get inspector name
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Tu Nombre ]';

        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen-word`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis: currentAnalysis,
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString('es-MX'),
                    inspector_name: inspectorName
                }
            })
        });

        const data = await response.json();

        if (data.success) {
            // Download file
            window.location.href = `/api/download/${data.filename}`;
        } else {
            alert('Error generando dictamen Word: ' + data.error);
        }

    } catch (error) {
        console.error('Error:', error);
        alert('Error al generar dictamen Word');
    }
}

function newAnalysis() {
    // Reset
    selectedImage = null;
    currentAnalysis = null;

    // Hide results
    document.getElementById('results-section').style.display = 'none';

    // Reset image
    document.getElementById('image-preview').style.display = 'none';
    document.querySelector('.upload-placeholder').style.display = 'block';
    document.getElementById('analyze-btn').disabled = true;

    // Reset steps
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById(`step-${i}`);
        if (i === 1) {
            step.textContent = '✓ Imagen recibida';
        } else {
            step.textContent = step.textContent.replace('✓', '⏳');
        }
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

async function updateStep(stepNum, text) {
    const step = document.getElementById(`step-${stepNum}`);
    if (step) {
        step.textContent = text;
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function checkServerHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/health`);
        const data = await response.json();
        console.log('Server health:', data);
    } catch (error) {
        console.warn('Could not connect to server. Running in standalone mode.');
    }
}

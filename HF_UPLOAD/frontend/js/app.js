// Main application JavaScript

// API Configuration
const API_BASE_URL = window.location.origin; // Uses current origin (http://localhost:8080)

let selectedImages = []; // Array of File objects or URL strings
const MAX_IMAGES = 5;
let currentAnalysis = null;
let currentImageFilenames = [];

// Initialize app
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    const imageInput = document.getElementById('image-input');
    const uploadArea = document.getElementById('upload-area');
    const analyzeBtn = document.getElementById('analyze-btn');
    const addUrlBtn = document.getElementById('add-url-btn');

    // Image selection (File Input)
    imageInput.addEventListener('change', handleImageSelect);

    // URL Input
    addUrlBtn.addEventListener('click', handleUrlAdd);

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
            handleFiles(files);
        }
    });

    // Analyze button
    analyzeBtn.addEventListener('click', analyzeInstallation);
}

function handleImageSelect(e) {
    handleFiles(e.target.files);
    // Reset input so same files can be selected again if cleared
    e.target.value = ''; 
}

function handleFiles(files) {
    if (selectedImages.length + files.length > MAX_IMAGES) {
        alert(`Solo puedes subir un máximo de ${MAX_IMAGES} imágenes.`);
        return;
    }

    let added = 0;
    for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (!file.type.startsWith('image/')) {
            alert(`El archivo "${file.name}" no es una imagen válida.`);
            continue;
        }
        selectedImages.push(file);
        added++;
    }

    if (added > 0) {
        updateUI();
    }
}

async function handleUrlAdd() {
    const urlInput = document.getElementById('image-url');
    const url = urlInput.value.trim();

    if (!url) return;

    if (selectedImages.length >= MAX_IMAGES) {
        alert(`Límite de ${MAX_IMAGES} imágenes alcanzado.`);
        return;
    }

    // Basic validation
    try {
        new URL(url);
    } catch (_) {
        alert('Por favor ingresa una URL válida.');
        return;
    }

    // Optional: Check if it's an image (head request) or just add it
    // For simplicity, we assume it's an image. The backend will validate/download.
    selectedImages.push({ type: 'url', value: url });
    urlInput.value = '';
    updateUI();
}

function removeImage(index) {
    selectedImages.splice(index, 1);
    updateUI();
}

function updateUI() {
    const container = document.getElementById('image-preview-container');
    const placeholder = document.querySelector('.upload-placeholder');
    const analyzeBtn = document.getElementById('analyze-btn');
    const countLabel = document.getElementById('image-count');

    container.innerHTML = '';

    if (selectedImages.length === 0) {
        container.style.display = 'none';
        placeholder.style.display = 'block';
        analyzeBtn.disabled = true;
        countLabel.style.display = 'none';
    } else {
        placeholder.style.display = 'none';
        container.style.display = 'grid'; // Ensure grid display
        analyzeBtn.disabled = false;
        
        countLabel.textContent = `${selectedImages.length}/${MAX_IMAGES} imágenes seleccionadas`;
        countLabel.style.display = 'block';

        selectedImages.forEach((item, index) => {
            const div = document.createElement('div');
            div.className = 'preview-item';

            const img = document.createElement('img');
            
            if (item.type === 'url') {
                img.src = item.value;
                img.onerror = () => { img.src = 'assets/icons/error_image.png'; /* Fallback */ };
            } else {
                // File object
                const reader = new FileReader();
                reader.onload = (e) => { img.src = e.target.result; };
                reader.readAsDataURL(item);
            }

            const removeBtn = document.createElement('button');
            removeBtn.className = 'remove-btn';
            removeBtn.innerHTML = '×';
            removeBtn.onclick = () => removeImage(index);

            div.appendChild(img);
            div.appendChild(removeBtn);
            container.appendChild(div);
        });
    }
}

async function analyzeInstallation() {
    if (selectedImages.length === 0) {
        alert('Por favor selecciona al menos una imagen');
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
        await updateStep(1, '✓ Imágenes recibidas');
        await sleep(500);

        await updateStep(2, '⏳ Analizando elementos visuales...');

        // Prepare FormData
        const formData = new FormData();
        formData.append('installation_type', installationType);

        // Append files and URLs separately
        selectedImages.forEach((item) => {
            if (item.type === 'url') {
                formData.append('image_urls', item.value);
            } else {
                formData.append('images', item);
            }
        });

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
        currentImageFilenames = data.image_filenames || [];

        // Display results
        displayResults(data.analysis);
        
        // Setup download links for original photos
        setupPhotoDownloads(currentImageFilenames);

        // Hide loading, show results
        loading.style.display = 'none';
        analysisResults.style.display = 'block';

    } catch (error) {
        console.error('Error:', error);
        alert(`Error en el análisis: ${error.message}`);
        loading.style.display = 'none';
    }
}

function setupPhotoDownloads(filenames) {
    const container = document.getElementById('photo-links-container');
    const section = document.getElementById('photo-downloads');
    
    if (!filenames || filenames.length === 0) {
        section.style.display = 'none';
        return;
    }
    
    container.innerHTML = '';
    filenames.forEach((filename, index) => {
        const a = document.createElement('a');
        a.href = `/api/download-photo/${filename}`;
        a.className = 'photo-link';
        a.target = '_blank';
        a.textContent = `📥 Foto ${index + 1}`;
        a.download = filename; // Suggest filename
        container.appendChild(a);
    });
    
    section.style.display = 'block';
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

    // Acciones Sugeridas
    const actionsTab = document.getElementById('actions-tab');
    const actions = analysis.vision_analysis.acciones_sugeridas || analysis.vision_analysis.recommendations || [];

    if (actions && actions.length > 0) {
        actionsTab.innerHTML = '<ul>' +
            actions.map(action => `<li>• ${action}</li>`).join('') +
            '</ul>';
    } else {
        const dictamen = analysis.vision_analysis.dictamen || '';
        if (dictamen) {
            actionsTab.innerHTML = `<p>${dictamen}</p>`;
        } else {
            actionsTab.innerHTML = '<p>No se generaron acciones sugeridas específicas.</p>';
        }
    }

    // Observaciones Adicionales
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
    document.querySelectorAll('.tab-panel').forEach(panel => {
        panel.classList.remove('active');
    });
    document.querySelectorAll('.tab').forEach(tab => {
        tab.classList.remove('active');
    });

    document.getElementById(`${tabName}-tab`).classList.add('active');
    event.target.classList.add('active');
}

async function downloadDictamen() {
    if (!currentAnalysis) {
        alert('No hay análisis disponible');
        return;
    }

    try {
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Tu Nombre ]';

        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis: currentAnalysis,
                image_filenames: currentImageFilenames, // Send list of filenames
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString('es-MX'),
                    inspector_name: inspectorName
                }
            })
        });

        const data = await response.json();

        if (data.success) {
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
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Tu Nombre ]';

        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen-word`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                analysis: currentAnalysis,
                image_filenames: currentImageFilenames, // Send list of filenames
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString('es-MX'),
                    inspector_name: inspectorName
                }
            })
        });

        const data = await response.json();

        if (data.success) {
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
    selectedImages = [];
    currentAnalysis = null;
    currentImageFilenames = [];

    document.getElementById('results-section').style.display = 'none';
    updateUI();
    document.getElementById('image-url').value = '';

    // Reset steps
    for (let i = 1; i <= 4; i++) {
        const step = document.getElementById(`step-${i}`);
        if (i === 1) {
            step.textContent = '✓ Imagen recibida';
        } else {
            step.textContent = step.textContent.replace('✓', '⏳');
        }
    }

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
        console.warn('Could not connect to server.');
    }
}

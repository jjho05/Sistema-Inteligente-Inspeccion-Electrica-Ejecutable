// =====================================================
// Sistema de Inspección Eléctrica — app.js v2.0
// =====================================================

const API_BASE_URL = window.location.origin;

let selectedImage = null;
let currentAnalysis = null;
let currentImageFilenames = [];  // Array — stores all uploaded image filenames
let currentImagePaths = [];      // Full server-side paths for dictamen generation
let currentLanguage = 'es';

// ---- UI String Dictionaries ----
const UI_STRINGS = {
    es: {
        appTitle: '⚡ Sistema de Inspección Eléctrica',
        appSubtitle: 'Análisis automatizado con IA · Normativa NOM-001-SEDE-2012',
        labelNorm: '1. Normativa a Evaluar',
        labelType: '2. Selecciona el tipo de instalación',
        labelInspector: '3. Nombre del Inspector',
        labelImage: '4. Carga la imagen de la instalación',
        labelResults: 'Resultados del Análisis',
        labelClassification: 'Clasificación',
        labelSummary: 'Resumen',
        labelDetails: 'Detalles',
        uploadHint: '📸 Arrastra una imagen aquí o haz clic para seleccionar',
        selectBtn: 'Seleccionar Imagen',
        analyzeBtn: '⚡ Analizar Instalación',
        loadingText: 'Analizando instalación...',
        step1: '✓ Imagen recibida',
        step2: '⏳ Analizando elementos visuales...',
        step3: '⏳ Consultando normativa...',
        step4: '⏳ Generando dictamen...',
        step2done: '✓ Análisis visual completado',
        step3done: '✓ Verificación normativa completada',
        step4done: '✓ Dictamen generado',
        humanReviewTitle: 'REQUIERE REVISIÓN HUMANA',
        tabConformities: 'Conformidades',
        tabNonConformities: 'No Conformidades',
        tabObservations: 'Observaciones',
        tabActions: 'Acciones Sugeridas',
        tabAdditional: 'Obs. Adicionales',
        btnPdf: '📄 Descargar Dictamen (PDF)',
        btnWord: '📝 Descargar Dictamen (Word)',
        btnNew: '🔄 Nuevo Análisis',
        inspectorPlaceholder: 'Ingresa tu nombre completo',
        noConformities: 'No se registraron conformidades específicas.',
        noNonConformities: 'No se detectaron no conformidades.',
        noObservations: 'Sin observaciones adicionales.',
        noActions: 'No se generaron acciones sugeridas específicas.',
        noAdditional: 'No se identificaron observaciones adicionales.',
        errorNoImage: 'Por favor selecciona una imagen primero',
        errorInvalidImage: 'Por favor selecciona un archivo de imagen',
        errorAnalysis: 'Error en el análisis: ',
        errorNoDictamen: 'No hay análisis disponible',
        errorDictamen: 'Error generando dictamen: ',
        errorDictamenWord: 'Error generando dictamen Word: ',
        footerSub: 'Sistema Multi-Agente de IA para Inspección Eléctrica',
    },
    en: {
        appTitle: '⚡ Electrical Inspection System',
        appSubtitle: 'AI-powered automated analysis · NOM-001-SEDE-2012 / NEC Standards',
        labelNorm: '1. Applicable Standard',
        labelType: '2. Select installation type',
        labelInspector: '3. Inspector Name',
        labelImage: '4. Upload installation image',
        labelResults: 'Analysis Results',
        labelClassification: 'Classification',
        labelSummary: 'Summary',
        labelDetails: 'Details',
        uploadHint: '📸 Drag an image here or click to select',
        selectBtn: 'Select Image',
        analyzeBtn: '⚡ Start Technical Diagnosis',
        loadingText: 'Analyzing installation...',
        step1: '✓ Image received',
        step2: '⏳ Analyzing visual elements...',
        step3: '⏳ Checking standards...',
        step4: '⏳ Generating technical report...',
        step2done: '✓ Visual analysis complete',
        step3done: '✓ Standards verification complete',
        step4done: '✓ Technical report generated',
        humanReviewTitle: 'HUMAN REVIEW REQUIRED',
        tabConformities: 'Conformities',
        tabNonConformities: 'Non-Conformities',
        tabObservations: 'Observations',
        tabActions: 'Suggested Actions',
        tabAdditional: 'Additional Notes',
        btnPdf: '📄 Download Report (PDF)',
        btnWord: '📝 Download Report (Word)',
        btnNew: '🔄 New Analysis',
        inspectorPlaceholder: 'Enter your full name',
        noConformities: 'No specific conformities were recorded.',
        noNonConformities: 'No non-conformities were detected.',
        noObservations: 'No additional observations.',
        noActions: 'No specific suggested actions were generated.',
        noAdditional: 'No additional observations were identified.',
        errorNoImage: 'Please select an image first',
        errorInvalidImage: 'Please select an image file',
        errorAnalysis: 'Analysis error: ',
        errorNoDictamen: 'No analysis available',
        errorDictamen: 'Error generating report: ',
        errorDictamenWord: 'Error generating Word report: ',
        footerSub: 'Multi-Agent AI System for Electrical Inspection',
    }
};

function t(key) {
    return (UI_STRINGS[currentLanguage] || UI_STRINGS['es'])[key] || key;
}

// ---- Language Switcher ----
function setLanguage(lang) {
    currentLanguage = lang;
    document.getElementById('html-root').lang = lang;

    // Toggle button active states
    document.getElementById('lang-es').classList.toggle('active', lang === 'es');
    document.getElementById('lang-en').classList.toggle('active', lang === 'en');

    // Update all UI text
    applyUIStrings();
}

function applyUIStrings() {
    const set = (id, key) => {
        const el = document.getElementById(id);
        if (el) el.textContent = t(key);
    };
    const setPlaceholder = (id, key) => {
        const el = document.getElementById(id);
        if (el) el.placeholder = t(key);
    };

    set('app-title', 'appTitle');
    set('app-subtitle', 'appSubtitle');
    set('label-norm', 'labelNorm');
    set('label-type', 'labelType');
    set('label-inspector', 'labelInspector');
    set('label-image', 'labelImage');
    set('label-results', 'labelResults');
    set('label-classification', 'labelClassification');
    set('label-summary', 'labelSummary');
    set('label-details', 'labelDetails');
    set('upload-hint', 'uploadHint');
    set('select-btn', 'selectBtn');
    set('analyze-btn', 'analyzeBtn');
    set('loading-text', 'loadingText');
    set('human-review-title', 'humanReviewTitle');
    set('tab-btn-conformities', 'tabConformities');
    set('tab-btn-non-conformities', 'tabNonConformities');
    set('tab-btn-observations', 'tabObservations');
    set('tab-btn-actions', 'tabActions');
    set('tab-btn-additional', 'tabAdditional');
    set('btn-pdf', 'btnPdf');
    set('btn-word', 'btnWord');
    set('btn-new', 'btnNew');
    set('footer-sub', 'footerSub');
    setPlaceholder('inspector-name', 'inspectorPlaceholder');

    // Re-render analyze button text but keep disabled state
    const analyzeBtn = document.getElementById('analyze-btn');
    if (analyzeBtn) analyzeBtn.textContent = t('analyzeBtn');
}

// ---- Init ----
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkServerHealth();
});

function setupEventListeners() {
    const imageInput = document.getElementById('image-input');
    const uploadArea = document.getElementById('upload-area');
    const analyzeBtn = document.getElementById('analyze-btn');

    imageInput.addEventListener('change', handleImageSelect);

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
        } else {
            // Handle image URL drag from Google Images
            const url = e.dataTransfer.getData('text/uri-list');
            if (url) {
                handleImageUrl(url);
            }
        }
    });

    // Support paste (Ctrl+V) anywhere on the page
    document.addEventListener('paste', (e) => {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
            if (items[i].type.indexOf('image') !== -1) {
                const blob = items[i].getAsFile();
                handleImageFile(blob);
                break;
            }
        }
    });

    analyzeBtn.addEventListener('click', analyzeInstallation);
}

function handleImageSelect(e) {
    const file = e.target.files[0];
    if (file) handleImageFile(file);
}

function handleImageFile(file) {
    if (!file.type.startsWith('image/')) {
        alert(t('errorInvalidImage'));
        return;
    }

    selectedImage = file;
    document.getElementById('dropped-url').value = ''; // clear any URL

    const reader = new FileReader();
    reader.onload = (e) => {
        showPreview(e.target.result);
    };
    reader.readAsDataURL(file);
}

function handleImageUrl(url) {
    selectedImage = null;
    document.getElementById('dropped-url').value = url;
    showPreview(url);
}

function showPreview(src) {
    const preview = document.getElementById('image-preview');
    const previewImg = document.getElementById('preview-img');
    const placeholder = document.querySelector('.upload-placeholder');

    previewImg.src = src;
    preview.style.display = 'block';
    placeholder.style.display = 'none';
    document.getElementById('analyze-btn').disabled = false;
}

// ---- Analysis ----
async function analyzeInstallation() {
    const droppedUrl = document.getElementById('dropped-url') ? document.getElementById('dropped-url').value : '';
    if (!selectedImage && !droppedUrl) {
        alert(t('errorNoImage'));
        return;
    }

    const installationType = document.getElementById('installation-type').value;
    const resultsSection = document.getElementById('results-section');
    const loading = document.getElementById('loading');
    const analysisResults = document.getElementById('analysis-results');

    resultsSection.style.display = 'block';
    loading.style.display = 'block';
    analysisResults.style.display = 'none';
    resultsSection.scrollIntoView({ behavior: 'smooth' });

    try {
        await updateStep(1, '✓ ' + (currentLanguage === 'en' ? 'Image received' : 'Imagen recibida'), true);
        await sleep(300);
        await updateStep(2, t('step2'), true);

        const formData = new FormData();
        if (selectedImage) {
            formData.append('image', selectedImage);
        } else if (droppedUrl) {
            formData.append('image_urls', droppedUrl);
        }
        formData.append('installation_type', installationType);
        formData.append('language', currentLanguage);

        const response = await fetch(`${API_BASE_URL}/api/analyze`, {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            // Check for Hugging Face 504 Timeout
            if (response.status === 504) {
                throw new Error(currentLanguage === 'en' 
                    ? "Hugging Face Timeout (60s). The image is too complex or the AI took too long. Try a clearer image." 
                    : "Tiempo de espera agotado (Timeout Hugging Face). La imagen tardó más de 60 segundos en procesarse. Intenta con una imagen más clara.");
            }
        }

        const data = await response.json();

        if (!response.ok || !data.success) {
            throw new Error(data.error || `Server error (${response.status})`);
        }

        await updateStep(2, t('step2done'), true);
        await updateStep(3, t('step3'), true);
        await sleep(900);

        await updateStep(3, t('step3done'), true);
        await updateStep(4, t('step4'), true);
        await sleep(400);
        await updateStep(4, t('step4done'), true);

        currentAnalysis = data.analysis;
        // Store ALL image filenames and full paths returned by server
        currentImageFilenames = data.image_filenames || (data.image_filename ? [data.image_filename] : []);
        currentImagePaths = data.image_paths || [];

        displayResults(data.analysis);

        loading.style.display = 'none';
        analysisResults.style.display = 'block';

    } catch (error) {
        console.error('Analysis error:', error);
        
        // Handle CORS / Network disconnected errors gracefully
        let errorMsg = error.message;
        if (errorMsg === "Failed to fetch" || errorMsg.includes("NetworkError")) {
            errorMsg = currentLanguage === 'en' 
                ? "Connection lost or Timeout. Hugging Face cuts connections after 60 seconds. Try a smaller/clearer image."
                : "Conexión perdida o Timeout. Hugging Face corta el servidor si tarda más de 60 segundos. Intenta con una imagen más pequeña o clara.";
        }
        
        alert(t('errorAnalysis') + errorMsg);
        loading.style.display = 'none';
        resultsSection.style.display = 'none';
    }
}

// ---- Display Results ----
function displayResults(analysis) {
    // Human Review
    const humanContainer = document.getElementById('human-review-container');
    const humanText = document.getElementById('human-review-text');
    const humanReview = analysis.vision_analysis && analysis.vision_analysis.human_review;

    if (humanReview && humanReview.trim().length > 0) {
        humanContainer.style.display = 'block';
        humanText.textContent = humanReview;
    } else {
        humanContainer.style.display = 'none';
    }

    // Classification
    const classification = analysis.classification;
    const statusBadge = document.getElementById('classification-status');
    const classificationText = document.getElementById('classification-text');

    statusBadge.textContent = classification.status;
    // Normalize class for CSS matching
    const statusClass = classification.status.toLowerCase()
        .replace(/\s+/g, '-')
        .replace('condicionalmente-conforme', 'condicionalmente-conforme')
        .replace('conditionally-compliant', 'conditionally-compliant')
        .replace('non-compliant', 'non-compliant')
        .replace('no-conforme', 'no-conforme')
        .replace('compliant', 'compliant')
        .replace('conforme', 'conforme');
    statusBadge.className = 'status-badge ' + statusClass;
    classificationText.textContent = classification.justification;

    // Summary — clean up raw markers
    const summaryContent = document.getElementById('summary-content');
    let summaryText = analysis.summary || '';
    summaryText = summaryText
        .replace(/={3,}/g, '')
        .replace(/^#+\s*/gm, '')
        .trim();
    summaryContent.innerHTML = `<div style="line-height:1.8; font-size:0.94em;">${summaryText.replace(/\n/g, '<br>')}</div>`;

    // Conformities
    const conformitiesTab = document.getElementById('conformities-tab');
    const conformities = analysis.vision_analysis.conformities || [];
    conformitiesTab.innerHTML = conformities.length > 0
        ? '<ul>' + conformities.map(c => `<li>✓ ${escapeHtml(c)}</li>`).join('') + '</ul>'
        : `<p>${t('noConformities')}</p>`;

    // Non-conformities
    const nonConformitiesTab = document.getElementById('non-conformities-tab');
    const nonConformities = analysis.verified_non_conformities || [];
    nonConformitiesTab.innerHTML = nonConformities.length > 0
        ? '<ul>' + nonConformities.map(nc => {
            const article = nc.article ? ` (${currentLanguage === 'en' ? 'Art.' : 'Art.'} ${nc.article})` : '';
            const severity = nc.severity || 'medium';
            const icon = severity === 'high' ? '🔴' : severity === 'medium' ? '🟡' : '🟢';
            return `<li>${icon} ${escapeHtml(nc.description)}${article}</li>`;
          }).join('') + '</ul>'
        : `<p>${t('noNonConformities')}</p>`;

    // Observations
    const observationsTab = document.getElementById('observations-tab');
    const observations = analysis.vision_analysis.observations || '';
    observationsTab.innerHTML = observations
        ? `<p>${escapeHtml(observations)}</p>`
        : `<p>${t('noObservations')}</p>`;

    // Suggested Actions
    const actionsTab = document.getElementById('actions-tab');
    const actions = analysis.vision_analysis.acciones_sugeridas
        || analysis.vision_analysis.recommendations
        || analysis.vision_analysis.suggested_actions
        || [];
    if (actions && actions.length > 0) {
        actionsTab.innerHTML = '<ul>' + actions.map(a => `<li>• ${escapeHtml(a)}</li>`).join('') + '</ul>';
    } else {
        const dictamen = analysis.vision_analysis.dictamen || '';
        actionsTab.innerHTML = dictamen
            ? `<p>${escapeHtml(dictamen)}</p>`
            : `<p>${t('noActions')}</p>`;
    }

    // Additional Observations
    const additionalTab = document.getElementById('additional-tab');
    const additionalObs = analysis.vision_analysis.observaciones_adicionales || analysis.vision_analysis.additional_observations || '';
    const risks = analysis.vision_analysis.risks || [];
    if (additionalObs) {
        additionalTab.innerHTML = `<p>${escapeHtml(additionalObs)}</p>`;
    } else if (risks && risks.length > 0) {
        additionalTab.innerHTML = '<ul>' + risks.map(r => `<li>⚠️ ${escapeHtml(r)}</li>`).join('') + '</ul>';
    } else {
        additionalTab.innerHTML = `<p>${t('noAdditional')}</p>`;
    }
}

// ---- Tab Switcher ----
function showTab(tabName, btnEl) {
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(`${tabName}-tab`).classList.add('active');
    if (btnEl) btnEl.classList.add('active');
}

// ---- Downloads ----
async function downloadDictamen() {
    if (!currentAnalysis) { alert(t('errorNoDictamen')); return; }

    try {
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Inspector ]';
        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                analysis: currentAnalysis,
                image_filenames: currentImageFilenames,
                image_paths: currentImagePaths,
                image_filename: currentImageFilenames[0] || null,
                language: currentLanguage,
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString(currentLanguage === 'en' ? 'en-US' : 'es-MX'),
                    inspector_name: inspectorName
                }
            })
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = `/api/download/${data.filename}`;
        } else {
            alert(t('errorDictamen') + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(t('errorDictamen') + error.message);
    }
}

async function downloadDictamenWord() {
    if (!currentAnalysis) { alert(t('errorNoDictamen')); return; }

    try {
        const inspectorName = document.getElementById('inspector-name').value.trim() || '[ Inspector ]';
        const response = await fetch(`${API_BASE_URL}/api/generate-dictamen-word`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                analysis: currentAnalysis,
                image_filenames: currentImageFilenames,
                image_paths: currentImagePaths,
                image_filename: currentImageFilenames[0] || null,
                language: currentLanguage,
                inspection_data: {
                    folio: 'AUTO-' + Date.now(),
                    fecha: new Date().toLocaleDateString(currentLanguage === 'en' ? 'en-US' : 'es-MX'),
                    inspector_name: inspectorName
                }
            })
        });
        const data = await response.json();
        if (data.success) {
            window.location.href = `/api/download/${data.filename}`;
        } else {
            alert(t('errorDictamenWord') + data.error);
        }
    } catch (error) {
        console.error('Error:', error);
        alert(t('errorDictamenWord') + error.message);
    }
}

// ---- New Analysis ----
function newAnalysis() {
    selectedImage = null;
    currentAnalysis = null;
    currentImageFilenames = [];
    currentImagePaths = [];
    if (document.getElementById('dropped-url')) {
        document.getElementById('dropped-url').value = '';
    }

    document.getElementById('results-section').style.display = 'none';
    document.getElementById('image-preview').style.display = 'none';
    document.querySelector('.upload-placeholder').style.display = 'block';
    document.getElementById('analyze-btn').disabled = true;

    // Reset progress steps
    document.getElementById('step-1').textContent = t('step1');
    document.getElementById('step-2').textContent = t('step2');
    document.getElementById('step-3').textContent = t('step3');
    document.getElementById('step-4').textContent = t('step4');
    document.querySelectorAll('.step').forEach(s => s.classList.remove('step-active', 'step-done'));

    // Reset tabs
    document.querySelectorAll('.tab-panel').forEach((p, i) => p.classList.toggle('active', i === 0));
    document.querySelectorAll('.tab').forEach((t, i) => t.classList.toggle('active', i === 0));

    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ---- Helpers ----
async function updateStep(stepNum, text, isActive = false) {
    const step = document.getElementById(`step-${stepNum}`);
    if (!step) return;
    step.textContent = text;
    // Remove previous state classes
    step.classList.remove('step-active', 'step-done');
    if (isActive && text.startsWith('⏳')) {
        step.classList.add('step-active');
    } else if (isActive && (text.startsWith('✓') || text.includes('✓'))) {
        step.classList.add('step-done');
    }
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function escapeHtml(str) {
    if (typeof str !== 'string') return String(str || '');
    return str
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
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

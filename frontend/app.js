const API_URL = 'http://localhost:5000';

const keywordsInput = document.getElementById('keywords');
const locationSelect = document.getElementById('location');
const jobTypeSelect = document.getElementById('jobType');
const technologySelect = document.getElementById('technology');
const searchBtn = document.getElementById('searchBtn');
const jobsList = document.getElementById('jobsList');
const resultsCount = document.getElementById('resultsCount');
const loading = document.getElementById('loading');
const errorDiv = document.getElementById('error');

let locations = [];
let technologies = [];

async function loadFilterOptions() {
    try {
        const response = await fetch(`${API_URL}/jobs/filters/options`);
        if (!response.ok) throw new Error('Error cargando filtros');

        const data = await response.json();

        locations = data.locations || [];
        technologies = data.technologies || [];

        populateSelect(locationSelect, locations);
        populateSelect(technologySelect, technologies);

    } catch (err) {
        console.error('Error cargando filtros:', err);
        loadDefaultFilters();
    }
}

function populateSelect(select, options) {
    const firstOption = select.options[0];
    select.innerHTML = '';
    select.appendChild(firstOption);

    options.forEach(opt => {
        const option = document.createElement('option');
        option.value = opt;
        option.textContent = opt;
        select.appendChild(option);
    });
}

function loadDefaultFilters() {
    const defaultLocations = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Remote'];
    const defaultTechs = ['Python', 'JavaScript', 'React', 'Node.js', 'Java', 'SQL', 'AWS', 'Docker'];

    populateSelect(locationSelect, defaultLocations);
    populateSelect(technologySelect, defaultTechs);
}

async function searchJobs() {
    showLoading();
    hideError();

    const searchRequest = {
        keywords: keywordsInput.value.trim(),
        location: locationSelect.value,
        job_type: jobTypeSelect.value || null,
        technologies: technologySelect.value ? [technologySelect.value] : null,
        page: 1
    };

    try {
        const response = await fetch(`${API_URL}/jobs/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchRequest)
        });

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}));
            throw new Error(errorData.detail || `Error ${response.status}`);
        }

        const data = await response.json();
        displayJobs(data.jobs, data.total_count);

    } catch (err) {
        showError('No se pudo conectar con el servidor. Asegúrate de que el backend esté funcionando en http://localhost:5000');
        console.error('Search error:', err);
    } finally {
        hideLoading();
    }
}

function displayJobs(jobs, total) {
    jobsList.innerHTML = '';
    resultsCount.textContent = `${total} resultado${total !== 1 ? 's' : ''}`;

    if (jobs.length === 0) {
        jobsList.innerHTML = '<p class="no-results">No se encontraron trabajos con esos criterios.</p>';
        return;
    }

    jobs.forEach(job => {
        const card = document.createElement('div');
        card.className = 'job-card';

        const typeClass = job.job_type || 'on-site';
        const salary = job.salary ? `<span class="job-salary">${job.salary}</span>` : '';
        const date = job.posted_date ? `<span class="job-date">${formatDate(job.posted_date)}</span>` : '';

        card.innerHTML = `
            <div class="job-header">
                <div>
                    <h3 class="job-title">${escapeHtml(job.title)}</h3>
                    <span class="job-company">${escapeHtml(job.company)}</span>
                </div>
                <span class="job-type ${typeClass}">${getTypeLabel(job.job_type)}</span>
            </div>
            <div class="job-meta">
                <span>📍 ${escapeHtml(job.location || 'No especificada')}</span>
                <span>📅 ${date}</span>
                <span>📡 ${job.source}</span>
            </div>
            <p class="job-description">${escapeHtml(job.description)}</p>
            <div class="job-footer">
                ${salary}
                ${date}
            </div>
            ${job.url ? `<a href="${escapeHtml(job.url)}" target="_blank" class="job-link">Ver oferta →</a>` : ''}
        `;

        jobsList.appendChild(card);
    });
}

function getTypeLabel(type) {
    const labels = {
        'remote': 'Remoto',
        'hybrid': 'Híbrido',
        'on-site': 'Presencial',
        'fulltime': 'Tiempo completo'
    };
    return labels[type] || type || 'No especificado';
}

function formatDate(dateStr) {
    if (!dateStr) return '';
    try {
        const date = new Date(dateStr);
        return date.toLocaleDateString('es-ES', { day: 'numeric', month: 'short', year: 'numeric' });
    } catch {
        return dateStr;
    }
}

function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function showLoading() {
    jobsList.innerHTML = '';
    loading.classList.remove('hidden');
}

function hideLoading() {
    loading.classList.add('hidden');
}

function showError(message) {
    errorDiv.textContent = message;
    errorDiv.classList.remove('hidden');
}

function hideError() {
    errorDiv.classList.add('hidden');
}

searchBtn.addEventListener('click', searchJobs);

keywordsInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') searchJobs();
});

document.addEventListener('DOMContentLoaded', () => {
    loadFilterOptions();
    searchJobs();
});

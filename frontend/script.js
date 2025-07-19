const API_BASE_URL = 'http://localhost:8000';

function getToken() {
    return localStorage.getItem('token');
}

function setToken(token) {
    localStorage.setItem('token', token);
}

function removeToken() {
    localStorage.removeItem('token');
}

function showError(elementId, message) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.textContent = message;
        errorElement.style.display = 'block';
    }
}

function hideError(elementId) {
    const errorElement = document.getElementById(elementId);
    if (errorElement) {
        errorElement.style.display = 'none';
    }
}

function checkAuth() {
    const token = getToken();
    const currentPage = window.location.pathname.split('/').pop();
    
    if (!token && currentPage === 'dashboard.html') {
        window.location.href = 'index.html';
        return false;
    }
    
    if (token && (currentPage === 'index.html' || currentPage === '')) {
        window.location.href = 'dashboard.html';
        return false;
    }
    
    return true;
}

async function login(username, password) {
    try {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password
            })
        });

        if (!response.ok) {
            throw new Error('Usuário ou senha incorretos');
        }

        const data = await response.json();
        setToken(data.access_token);
        window.location.href = 'dashboard.html';
        
    } catch (error) {
        showError('loginError', error.message);
    }
}

function logout() {
    removeToken();
    window.location.href = 'index.html';
}

async function uploadContract(file) {
    const token = getToken();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const formData = new FormData();
        formData.append('file', file);

        const response = await fetch(`${API_BASE_URL}/contracts/upload`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`
            },
            body: formData
        });

        if (!response.ok) {
            if (response.status === 401) {
                logout();
                return;
            }
            throw new Error('Erro ao fazer upload do contrato');
        }

        const data = await response.json();
        displayContractAnalysis(data);
        
    } catch (error) {
        showError('uploadError', error.message);
        hideUploadProgress();
    }
}

async function searchContract() {
    const contractName = document.getElementById('searchInput').value;
    if (!contractName) {
        alert('Digite o nome do contrato');
        return;
    }

    const token = getToken();
    if (!token) {
        window.location.href = 'index.html';
        return;
    }

    try {
        const response = await fetch(`${API_BASE_URL}/contracts/${encodeURIComponent(contractName)}`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });

        if (!response.ok) {
            if (response.status === 401) {
                logout();
                return;
            }
            if (response.status === 404) {
                throw new Error('Contrato não encontrado');
            }
            throw new Error('Erro ao buscar contrato');
        }

        const data = await response.json();
        displaySearchResults(data);
        
    } catch (error) {
        document.getElementById('searchResults').innerHTML = `
            <div class="error-message">${error.message}</div>
        `;
    }
}

function displayContractAnalysis(contract) {
    const resultsSection = document.getElementById('resultsSection');
    const analysisContainer = document.getElementById('contractAnalysis');
    
    const analysisHTML = `
        <div class="analysis-item">
            <h3>📁 Nome do Arquivo</h3>
            <p>${contract.filename}</p>
        </div>
        <div class="analysis-item">
            <h3>👥 Partes do Contrato</h3>
            <p>${contract.nome_partes || 'Não identificado'}</p>
        </div>
        <div class="analysis-item">
            <h3>💰 Valores Monetários</h3>
            <p>${contract.valores_monetarios || 'Não identificado'}</p>
        </div>
        <div class="analysis-item">
            <h3>📋 Obrigações Principais</h3>
            <p>${contract.obrigacoes_principais || 'Não identificado'}</p>
        </div>
        <div class="analysis-item">
            <h3>📄 Dados Adicionais</h3>
            <p>${contract.dados_adicionais || 'Não identificado'}</p>
        </div>
        <div class="analysis-item">
            <h3>⚖️ Cláusula de Rescisão</h3>
            <p>${contract.clausula_rescisao || 'Não identificado'}</p>
        </div>
    `;
    
    analysisContainer.innerHTML = analysisHTML;
    resultsSection.style.display = 'block';
    hideUploadProgress();
}

function displaySearchResults(contract) {
    const searchResults = document.getElementById('searchResults');
    
    const resultHTML = `
        <div class="contract-analysis">
            <div class="analysis-item">
                <h3>📁 Nome do Arquivo</h3>
                <p>${contract.filename}</p>
            </div>
            <div class="analysis-item">
                <h3>👥 Partes do Contrato</h3>
                <p>${contract.nome_partes || 'Não identificado'}</p>
            </div>
            <div class="analysis-item">
                <h3>💰 Valores Monetários</h3>
                <p>${contract.valores_monetarios || 'Não identificado'}</p>
            </div>
            <div class="analysis-item">
                <h3>📋 Obrigações Principais</h3>
                <p>${contract.obrigacoes_principais || 'Não identificado'}</p>
            </div>
            <div class="analysis-item">
                <h3>📄 Dados Adicionais</h3>
                <p>${contract.dados_adicionais || 'Não identificado'}</p>
            </div>
            <div class="analysis-item">
                <h3>⚖️ Cláusula de Rescisão</h3>
                <p>${contract.clausula_rescisao || 'Não identificado'}</p>
            </div>
        </div>
    `;
    
    searchResults.innerHTML = resultHTML;
}

function showUploadProgress() {
    document.getElementById('uploadProgress').style.display = 'block';
    hideError('uploadError');
}

function hideUploadProgress() {
    document.getElementById('uploadProgress').style.display = 'none';
}

document.addEventListener('DOMContentLoaded', function() {
    checkAuth();
    

    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            hideError('loginError');
            
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            await login(username, password);
        });
    }
    
    const uploadForm = document.getElementById('uploadForm');
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            hideError('uploadError');
            
            const fileInput = document.getElementById('contractFile');
            const file = fileInput.files[0];
            
            if (!file) {
                showError('uploadError', 'Selecione um arquivo');
                return;
            }
            
            const allowedTypes = ['application/pdf', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'];
            if (!allowedTypes.includes(file.type)) {
                showError('uploadError', 'Apenas arquivos PDF e DOCX são aceitos');
                return;
            }
            
            showUploadProgress();
            await uploadContract(file);
        });
        
        const fileInput = document.getElementById('contractFile');
        if (fileInput) {
            fileInput.addEventListener('change', function(e) {
                const fileName = e.target.files[0]?.name;
                const label = document.querySelector('.file-label span');
                if (fileName && label) {
                    label.textContent = fileName;
                }
            });
        }
    }
    
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                searchContract();
            }
        });
    }
}); 
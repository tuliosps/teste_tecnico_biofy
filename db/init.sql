CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE contracts (
    id SERIAL PRIMARY KEY,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    nome_partes TEXT,
    valores_monetarios TEXT,
    obrigacoes_principais TEXT,
    dados_adicionais TEXT,
    clausula_rescisao TEXT,
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id)
);

CREATE INDEX idx_contracts_filename ON contracts(filename);
CREATE INDEX idx_users_username ON users(username);

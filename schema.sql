-- ==========================================================
-- Esquema de Tablas para Alejo Barber en Supabase (PostgreSQL)
-- ==========================================================

-- 1. Tabla de Configuración del Negocio
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

-- 2. Tabla de Servicios
CREATE TABLE IF NOT EXISTS services (
    id       SERIAL PRIMARY KEY,
    name     TEXT    NOT NULL,
    price    INTEGER NOT NULL,
    duration INTEGER NOT NULL
);

-- 3. Tabla de Turnos (Citas)
CREATE TABLE IF NOT EXISTS appointments (
    id             SERIAL PRIMARY KEY,
    client_name    TEXT    NOT NULL,
    client_phone   TEXT    NOT NULL,
    service_id     INTEGER REFERENCES services(id),
    date           TEXT    NOT NULL,
    time           TEXT    NOT NULL,
    status         TEXT    DEFAULT 'pending',
    payment_method TEXT    DEFAULT 'efectivo',
    confirmed_at   TIMESTAMPTZ
);

-- 4. Tabla de Bloqueos de Horario
CREATE TABLE IF NOT EXISTS blocks (
    id          SERIAL PRIMARY KEY,
    type        TEXT NOT NULL,
    date        TEXT,
    day_of_week INTEGER,
    start_time  TEXT,
    end_time    TEXT
);

-- 5. Tabla de Ventas de Productos
CREATE TABLE IF NOT EXISTS sales (
    id           SERIAL PRIMARY KEY,
    product_name TEXT    NOT NULL,
    price        INTEGER NOT NULL,
    created_at   TIMESTAMPTZ DEFAULT NOW()
);

-- 6. Tabla de Gastos
CREATE TABLE IF NOT EXISTS expenses (
    id         SERIAL PRIMARY KEY,
    concept    TEXT    NOT NULL,
    amount     INTEGER NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 7. Tabla de Usuarios Administradores
CREATE TABLE IF NOT EXISTS users (
    id       SERIAL PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password TEXT        NOT NULL
);

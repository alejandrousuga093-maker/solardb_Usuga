CREATE TABLE IF NOT EXISTS lecturas (
    id BIGSERIAL PRIMARY KEY,
    dispositivo_id TEXT NOT NULL,
    fecha_hora TIMESTAMPTZ NOT NULL,
    temperatura_c NUMERIC(6,2),
    humedad_pct NUMERIC(6,2),
    origen TEXT NOT NULL DEFAULT 'simulador',
    creado_en TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CONSTRAINT humedad_rango CHECK (humedad_pct IS NULL OR humedad_pct BETWEEN 0 AND 100)
);

CREATE INDEX IF NOT EXISTS idx_lecturas_fecha_hora ON lecturas (fecha_hora);
CREATE INDEX IF NOT EXISTS idx_lecturas_dispositivo ON lecturas (dispositivo_id);

CREATE TABLE IF NOT EXISTS etl_log (
    id BIGSERIAL PRIMARY KEY,
    inicio TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    fin TIMESTAMPTZ,
    archivo TEXT NOT NULL,
    filas_leidas INTEGER NOT NULL DEFAULT 0,
    filas_insertadas INTEGER NOT NULL DEFAULT 0,
    estado TEXT NOT NULL DEFAULT 'EN_PROCESO',
    detalle TEXT
);

-- Ejecutar como propietario/administrador de la base lectura_demo.
-- Si el rol ya existe, CREATE ROLE puede avisar de que ya existe.
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_roles WHERE rolname = 'solar_lector') THEN
        CREATE ROLE solar_lector LOGIN;
    END IF;
END
$$;

GRANT CONNECT ON DATABASE lectura_demo TO solar_lector;
GRANT USAGE ON SCHEMA public TO solar_lector;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO solar_lector;

-- Aplicar permisos de lectura también a tablas futuras creadas por el usuario actual.
ALTER DEFAULT PRIVILEGES IN SCHEMA public
GRANT SELECT ON TABLES TO solar_lector;

-- No se conceden INSERT, UPDATE, DELETE, CREATE ni permisos de administración.

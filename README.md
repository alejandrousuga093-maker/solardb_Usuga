# SolarDB — Taller de consulta (Grupo 811)

## Objetivo
Simular una canalización ETL de telemetría IoT: extraer lecturas JSONL, validarlas y cargarlas en PostgreSQL con registro de ejecución y permisos de solo lectura.

## Requisitos
- Python 3.10 o superior
- PostgreSQL 15 o superior
- Paquete Python `psycopg` (instalar con `pip install "psycopg[binary]"`)
- Variables de entorno: `PGHOST`, `PGPORT`, `PGDATABASE`, `PGUSER`, `PGPASSWORD`

## Estructura
- `data/lecturas.jsonl`: datos de muestra
- `etl/simulador.py`: genera lecturas simuladas
- `etl/run_etl.py`: valida y carga los datos en una transacción
- `sql/01_tablas.sql`: tablas de destino y bitácora
- `sql/02_carga.sql`: consulta de verificación
- `sql/03_roles.sql`: rol de solo lectura
- `run_etl.sh` / `run_etl.bat`: ejecución con un comando

## Preparación
1. Crear una base de datos llamada `lectura_demo`.
2. Ejecutar los SQL en orden con un usuario administrador:
   `psql -d lectura_demo -f sql/01_tablas.sql`
   `psql -d lectura_demo -f sql/03_roles.sql`
3. Instalar la dependencia: `pip install "psycopg[binary]"`.
4. Configurar las variables de conexión en el entorno. No guardes contraseñas en el repositorio.
5. Ejecutar `./run_etl.sh` en Linux/macOS o `run_etl.bat` en Windows.

## Automatización por hora
En Linux, editar el cron con `crontab -e` y agregar una línea, ajustando la ruta absoluta:
`0 * * * * cd /ruta/al/repositorio && ./run_etl.sh >> etl_cron.log 2>&1`
En Windows, usar el Programador de tareas para ejecutar `run_etl.bat` cada hora.

## Evidencias para el PDF
- Captura de la ejecución de `run_etl.sh` o `run_etl.bat`.
- Captura de `SELECT * FROM etl_log ORDER BY id DESC LIMIT 5;`.
- Captura de un `SELECT` exitoso con el rol `solar_lector`.
- Captura del repositorio y de la sección Collaborators en GitHub.
- Enlace al repositorio y explicación breve de cada evidencia.

## GitHub
Crear un repositorio público llamado `solardb-apellido1-apellido2`, invitar al compañero como colaborador y hacer al menos tres commits descriptivos por integrante. Reemplazar los apellidos del nombre sugerido por los de la pareja.

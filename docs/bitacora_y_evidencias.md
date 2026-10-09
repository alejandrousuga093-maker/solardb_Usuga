# Bitácora y evidencias para el informe

## Ejecución
Comando: `./run_etl.sh` (Linux/macOS) o `run_etl.bat` (Windows).

Resultado esperado: `ETL OK: N lecturas procesadas.`

## Consulta de bitácora
```sql
SELECT id, inicio, fin, filas_leidas, filas_insertadas, estado, detalle
FROM etl_log ORDER BY id DESC LIMIT 5;
```

## Prueba de solo lectura
Conectar a `lectura_demo` usando el usuario `solar_lector` y ejecutar:
```sql
SELECT COUNT(*) FROM lecturas;
SELECT * FROM lecturas LIMIT 5;
```
Para demostrar la restricción, intentar una modificación en una tabla de prueba (no en datos importantes):
```sql
INSERT INTO lecturas (dispositivo_id, fecha_hora)
VALUES ('prueba', NOW());
```
La inserción debe ser rechazada por falta de privilegios.

## Texto sugerido para las capturas
1. **Ejecución:** el proceso valida el JSONL y carga las filas dentro de una transacción.
2. **Bitácora:** `etl_log` registra fecha, archivo, filas procesadas y estado de la ejecución.
3. **Gobernanza:** `solar_lector` puede consultar las tablas, pero no insertar ni modificar registros.

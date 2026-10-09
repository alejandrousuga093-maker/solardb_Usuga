-- Verificar últimas lecturas cargadas
SELECT id, dispositivo_id, fecha_hora, temperatura_c, humedad_pct, origen
FROM lecturas
ORDER BY fecha_hora DESC
LIMIT 20;

-- Resumen por dispositivo
SELECT dispositivo_id, COUNT(*) AS total_lecturas,
       ROUND(AVG(temperatura_c), 2) AS temperatura_promedio
FROM lecturas
GROUP BY dispositivo_id
ORDER BY dispositivo_id;

-- Revisar historial de ejecuciones ETL
SELECT id, inicio, fin, archivo, filas_leidas, filas_insertadas, estado, detalle
FROM etl_log
ORDER BY id DESC
LIMIT 10;

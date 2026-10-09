"""ETL de lecturas JSONL a PostgreSQL con transacción y bitácora."""
import json
import os
import sys
from pathlib import Path
import psycopg

ARCHIVO = Path(os.getenv("ETL_FILE", "data/lecturas.jsonl"))

def main():
    if not ARCHIVO.exists():
        raise FileNotFoundError(f"No existe el archivo de entrada: {ARCHIVO}")

    filas = []
    with ARCHIVO.open("r", encoding="utf-8") as entrada:
        for numero, linea in enumerate(entrada, start=1):
            if not linea.strip():
                continue
            try:
                dato = json.loads(linea)
                dispositivo = str(dato["dispositivo_id"]).strip()
                fecha = dato["fecha_hora"]
                temperatura = dato.get("temperatura_c")
                humedad = dato.get("humedad_pct")
                if not dispositivo or not fecha:
                    raise ValueError("dispositivo_id y fecha_hora son obligatorios")
                if humedad is not None and not 0 <= float(humedad) <= 100:
                    raise ValueError("humedad_pct debe estar entre 0 y 100")
                filas.append((dispositivo, fecha, temperatura, humedad))
            except (ValueError, KeyError, TypeError) as exc:
                raise ValueError(f"Error en la línea {numero}: {exc}") from exc

    conexion = psycopg.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "lectura_demo"),
        user=os.getenv("PGUSER", "postgres"),
        password=os.getenv("PGPASSWORD"),
    )
    try:
        with conexion:
            with conexion.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO etl_log (archivo, filas_leidas, estado) "
                    "VALUES (%s, %s, %s) RETURNING id",
                    (str(ARCHIVO), len(filas), "EN_PROCESO"),
                )
                log_id = cursor.fetchone()[0]
                cursor.executemany(
                    """INSERT INTO lecturas
                       (dispositivo_id, fecha_hora, temperatura_c, humedad_pct)
                       VALUES (%s, %s, %s, %s)""",
                    filas,
                )
                cursor.execute(
                    """UPDATE etl_log
                       SET fin = NOW(), filas_insertadas = %s, estado = %s,
                           detalle = %s
                       WHERE id = %s""",
                    (len(filas), "OK", "Carga completada", log_id),
                )
        print(f"ETL OK: {len(filas)} lecturas procesadas.")
    except Exception as exc:
        conexion.rollback()
        # Intentar registrar el error en una transacción separada.
        try:
            with conexion:
                with conexion.cursor() as cursor:
                    cursor.execute(
                        """INSERT INTO etl_log
                           (archivo, filas_leidas, filas_insertadas, estado, detalle, fin)
                           VALUES (%s, %s, 0, 'ERROR', %s, NOW())""",
                        (str(ARCHIVO), len(filas), str(exc)[:1000]),
                    )
        except Exception:
            pass
        print(f"ETL ERROR: {exc}", file=sys.stderr)
        raise
    finally:
        conexion.close()

if __name__ == "__main__":
    main()

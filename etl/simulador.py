"""Genera lecturas JSONL simuladas para probar el proceso ETL."""
import json
import random
from datetime import datetime, timezone

def main():
    now = datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")
    with open("data/lecturas.jsonl", "a", encoding="utf-8") as archivo:
        for dispositivo in ("sensor-01", "sensor-02"):
            fila = {
                "dispositivo_id": dispositivo,
                "fecha_hora": now,
                "temperatura_c": round(random.uniform(20, 32), 2),
                "humedad_pct": round(random.uniform(35, 85), 2),
            }
            archivo.write(json.dumps(fila, ensure_ascii=False) + "\\n")
    print("Lecturas simuladas agregadas a data/lecturas.jsonl")

if __name__ == "__main__":
    main()

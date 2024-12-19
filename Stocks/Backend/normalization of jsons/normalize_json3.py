import json
import re

# Percorso al file stocks3.json
file_path = "/Users/mustafa66/Desktop/IR---Project/Stocks/stocks/stocks3.json"

# Campi standard
standard_fields = ["name", "last", "percentage", "time", "low", "high", "opening", "volume", "market_gap"]

# Funzione per pulire i valori
def clean_value(value):
    if isinstance(value, str):
        # Rimuovi caratteri Unicode (\u00a0, spazi) e stringhe vuote
        value = re.sub(r"[\u00a0]", "", value).strip()
        # Restituisci `null` se la stringa è vuota
        if value == "":
            return None
        # Converti in numero se applicabile
        try:
            return float(value.replace(",", "")) if value.replace(",", "").replace(".", "").isdigit() else value
        except ValueError:
            return value
    return value if value is not None else None

# Carica il file JSON
with open(file_path, 'r') as f:
    data = json.load(f)

# Normalizza i documenti
for record in data:
    # Pulizia dei valori
    for key in record:
        record[key] = clean_value(record[key])

    # Aggiungi campi mancanti con valore `null`
    for field in standard_fields:
        if field not in record:
            record[field] = None

# Salva il file aggiornato
with open(file_path, 'w') as f:
    json.dump(data, f, indent=4)

print("Correzione e normalizzazione di stocks3.json completata.")
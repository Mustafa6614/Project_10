import json

# Percorso al file stocks.json
file_path = "/Users/mustafa66/Desktop/IR---Project/Stocks/stocks/stocks.json"

# Funzione per convertire stringhe vuote in null
def replace_empty_with_null(value):
    if value == "":  # Se il valore è una stringa vuota
        return None
    return value  # Altrimenti, ritorna il valore originale

# Leggi il file JSON
with open(file_path, 'r') as file:
    data = json.load(file)

# Aggiorna i valori nei record
for record in data:
    for key in record:
        record[key] = replace_empty_with_null(record[key])

# Salva il file aggiornato
with open(file_path, 'w') as file:
    json.dump(data, file, indent=4)

print("Le stringhe vuote sono state sostituite con null in stocks.json.")
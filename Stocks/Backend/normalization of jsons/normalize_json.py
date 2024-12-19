import json

# File paths
file_paths = {
    "stocks.json": "/Users/mustafa66/Desktop/IR---Project/Stocks/stocks/stocks.json",
    "stocks2.json": "/Users/mustafa66/Desktop/IR---Project/Stocks/stocks/stocks2.json",
    "stocks3.json": "/Users/mustafa66/Desktop/IR---Project/Stocks/stocks/stocks3.json"
}

# Struttura desiderata con tipo di dato predefinito
desired_structure = {
    "name": "",
    "last": None,
    "low": None,
    "high": None,
    "percentage": None,
    "volume": None,
    "market_gap": "",
    "opening": None,
    "time": ""
}


# Helper function to parse and normalize values
def normalize_value(key, value):
    if value is None or value == "":
        return None if desired_structure[key] is None else desired_structure[key]
    if key in ["last", "low", "high", "percentage", "volume", "opening"]:
        return float(value)  # Convert to float if numeric
    return str(value)  # Convert all other values to string


# Helper function to normalize a record
def normalize_record(record):
    normalized_record = {}
    for key in desired_structure:
        normalized_record[key] = normalize_value(key, record.get(key))
    return normalized_record


# Normalizza ciascun file JSON
for file_name, file_path in file_paths.items():
    print(f"Normalizing {file_name}...")
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Normalizzare ogni record
    normalized_data = [normalize_record(record) for record in data]

    # Salvare il file normalizzato
    with open(file_path, 'w') as file:
        json.dump(normalized_data, file, indent=4)

    print(f"{file_name} normalized successfully.")

print("All files have been normalized.")
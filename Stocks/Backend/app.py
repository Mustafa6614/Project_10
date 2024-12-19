from flask import Flask, request, jsonify
from flask_cors import CORS
from solr_client import SolrClient
import requests

app = Flask(__name__)
CORS(app)
solr = SolrClient("http://localhost:8983/solr", "stocks")

@app.route('/search', methods=['GET'])
def search():
    attribute = request.args.get('attribute', 'name')  # Attributo di default
    value = request.args.get('value', '*')  # Valore cercato
    rows = int(request.args.get('rows', 10))  # Numero di risultati per pagina
    start = int(request.args.get('start', 0))  # Offset per la paginazione

    # Determina il tipo di query basandosi sull'attributo
    if attribute == "name" and value != "*":
        if " " in value:  # Se il valore contiene spazi
            query = f'name_str:"{value}"'
        else:
            query = f'name_str:{value}*'
    elif attribute in ["last", "low", "high", "percentage", "volume", "opening"]:
        if value.isdigit():
            base_value = float(value)
            range_end = base_value + 0.999999
            query = f"{attribute}:[{base_value} TO {range_end}]"
        else:
            query = f"{attribute}:{value}"
    else:
        query = f"{attribute}:{value}*" if value != "*" else "*:*"

    # Configura i parametri della richiesta
    params = {
        "q": query,
        "rows": rows,
        "start": start,
        "sort": "name_str asc",  # Ordina per il campo name_str in ordine crescente
        "wt": "json"  # Formato di risposta
    }

    try:
        # Invia la richiesta HTTP a Solr
        response = requests.get("http://localhost:8983/solr/stocks/select", params=params)
        response.raise_for_status()
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/recommend', methods=['GET'])
def recommend():
    attribute = request.args.get('attribute', 'last')
    value = request.args.get('value', type=float)
    range_percent = request.args.get('range', default=0.1, type=float)

    # Calcola il range
    min_value = value * (1 - range_percent)
    max_value = value * (1 + range_percent)

    print(f"Query range: {min_value} TO {max_value}")  # Log per debug

    query = f"{attribute}:[{min_value} TO {max_value}]"
    solr_response = solr.search(query, rows=5)  # Query Solr

    print(f"Results: {solr_response['response']['docs']}")
    return jsonify(solr_response['response']['docs'])

if __name__ == '__main__':
    app.run(port=5000, debug=True)
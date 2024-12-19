import requests

class SolrClient:
    def __init__(self, solr_url, core_name):
        self.base_url = f"http://localhost:8983/solr/stocks/select"

    def search(self, query, rows=10, start=0):  # Aggiunto il parametro 'start'
        params = {
            "q": query,
            "wt": "json",
            "rows": rows,
            "start": start  # Aggiunto il parametro 'start'
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            return {"error": str(e)}

if __name__ == "__main__":
    solr = SolrClient("http://localhost:8983/solr", "stocks")
    query = input("Enter search query: ")
    results = solr.search(query)
    print(results)

// Variabili globali
let currentFilter = ""; // Lettera attuale selezionata
let currentSearchAttribute = "name"; // Attributo di default
let currentSearchValue = "*"; // Valore di default
let currentPage = 0; // Pagina corrente
const rowsPerPage = 20; // Risultati per pagina

// Funzione per eseguire la ricerca
function performSearch() {
    const attribute = currentSearchAttribute;
    let searchValue = currentSearchValue;
    
    if (attribute === "name") {
        searchValue = capitalizeEachWord(searchValue);
    }
    
    // Applica il filtro alfabetico se presente
    if (currentFilter) {
        if (attribute === "name") {
            searchValue = `${currentFilter}${searchValue === "*" ? "*" : searchValue}`;
        } else {
            searchValue = `${currentSearchValue}`;
        }
    }
    
    fetch(`http://127.0.0.1:5000/search?attribute=${attribute}&value=${searchValue}&rows=${rowsPerPage}&start=${currentPage * rowsPerPage}`)
        .then(response => response.json())
        .then(data => {
            const results = data.response.docs;
            const resultsContainer = document.getElementById("results");
            const paginationContainer = document.getElementById("pagination");

            resultsContainer.innerHTML = ""; // Pulisce i risultati precedenti
            paginationContainer.innerHTML = ""; // Pulisce la sezione di paginazione precedente

            if (results.length === 0) {
                resultsContainer.innerHTML = "<p>No results found for your query.</p>";
                const recommendationsContainer = document.getElementById("recommendations");
                recommendationsContainer.innerHTML = "<p>No recommendations available.</p>"; // Nessuna raccomandazione
            } else {
                let tableHTML = `
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Last Price</th>
                                <th>High</th>
                                <th>Low</th>
                                <th>Opening</th>
                                <th>Percentage</th>
                                <th>Time</th>
                                <th>Volume</th>
                                <th>Market Gap</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                results.forEach(stock => {
                    const stockName = Array.isArray(stock.name) ? stock.name[0] : stock.name;
                    let link = null;

                    // Link per specifici stocks
                    if (stockName && typeof stockName === "string") {
                        if (stockName.toLowerCase().trim() === "adidas") {
                            link = "https://www.borsaitaliana.it/borsa/azioni/global-equity-market/scheda/DE000A1EWWW0.html?lang=en";
                        } else if (stockName.toLowerCase().trim() === "juventus fc") {
                            link = "https://www.borsaitaliana.it/borsa/azioni/scheda/IT0005572778.html?lang=en";
                        } else if (stockName.toLowerCase().trim() === "ferrari") {
                            link = "https://www.borsaitaliana.it/borsa/azioni/scheda/NL0011585146.html?lang=en";
                        }
                    }

                    // Genera la riga della tabella
                    tableHTML += `
                        <tr>
                            <td>${link ? `<a href="${link}" target="_blank" style="color: #007bff; text-decoration: none;">${stockName}</a>` : stockName || "N/A"}</td>
                            <td>${stock.last ? stock.last[0] : "N/A"}</td>
                            <td>${stock.high ? stock.high[0] : "N/A"}</td>
                            <td>${stock.low ? stock.low[0] : "N/A"}</td>
                            <td>${stock.opening ? stock.opening[0] : "N/A"}</td>
                            <td>${stock.percentage ? stock.percentage[0] : "N/A"}</td>
                            <td>${stock.time ? stock.time[0] : "N/A"}</td>
                            <td>${stock.volume ? stock.volume[0] : "N/A"}</td>
                            <td>${stock.market_gap || "N/A"}</td>
                        </tr>
                    `;
                });

                tableHTML += `</tbody></table>`;
                resultsContainer.innerHTML = tableHTML;

                if (results.length == 1) {
                    const firstResult = results[0];
                    if (firstResult.last) {
                        fetchRecommendations("last", firstResult.last[0]);
                    } else if (firstResult.volume) {
                        fetchRecommendations("volume", firstResult.volume[0]);
                    } else {
                        const recommendationsContainer = document.getElementById("recommendations");
                        recommendationsContainer.innerHTML = "<p>No recommendations available.</p>";
                    }
                } else {
                    const recommendationsContainer = document.getElementById("recommendations");
                    recommendationsContainer.innerHTML = "<p>Recommendations are displayed only for one result.</p>";
                }
            }

            // Mostra i pulsanti di paginazione
            paginationContainer.innerHTML = `
                <div class="pagination">
                    <button ${currentPage === 0 ? "disabled" : ""} onclick="changePage(-1)">Previous</button>
                    <button ${results.length === rowsPerPage ? "" : "disabled"} onclick="changePage(1)">Next</button>
                </div>
            `;
        })
        .catch(error => console.error("Error fetching search results:", error));
}

function fetchRecommendations(attribute, value) {
    fetch(`http://127.0.0.1:5000/recommend?attribute=${attribute}&value=${value}&range=0.1`)
        .then(response => response.json())
        .then(data => {
            const recommendationsContainer = document.getElementById("recommendations");
            recommendationsContainer.innerHTML = ""; // Resetta il contenitore

            // Escludi il titolo cercato
            const filteredData = data.filter(stock => {
                const stockName = stock.name ? stock.name[0].toLowerCase() : "";
                const currentResults = Array.from(document.querySelectorAll("#results tbody tr td:first-child")).map(td => td.textContent.trim().toLowerCase());
                return !currentResults.includes(stockName); // Escludi i nomi già presenti nei risultati principali
            });

            if (filteredData.length === 0) {
                recommendationsContainer.innerHTML = "<p>No recommendations available.</p>";
            } else {
                // Genera una tabella per le raccomandazioni
                let tableHTML = `
                    <h3>Recommended Stocks</h3>
                    <table>
                        <thead>
                            <tr>
                                <th>Name</th>
                                <th>Last Price</th>
                                <th>High</th>
                                <th>Low</th>
                                <th>Opening</th>
                                <th>Percentage</th>
                                <th>Time</th>
                                <th>Volume</th>
                                <th>Market Gap</th>
                            </tr>
                        </thead>
                        <tbody>
                `;

                filteredData.forEach(stock => {
                    tableHTML += `
                        <tr>
                            <td>${stock.name ? stock.name[0] : "N/A"}</td>
                            <td>${stock.last ? stock.last[0] : "N/A"}</td>
                            <td>${stock.high ? stock.high[0] : "N/A"}</td>
                            <td>${stock.low ? stock.low[0] : "N/A"}</td>
                            <td>${stock.opening ? stock.opening[0] : "N/A"}</td>
                            <td>${stock.percentage ? stock.percentage[0] : "N/A"}</td>
                            <td>${stock.time ? stock.time[0] : "N/A"}</td>
                            <td>${stock.volume ? stock.volume[0] : "N/A"}</td>
                            <td>${stock.market_gap || "N/A"}</td>
                        </tr>
                    `;
                });

                tableHTML += `</tbody></table>`;
                recommendationsContainer.innerHTML = tableHTML;
            }
        })
        .catch(error => console.error("Error fetching recommendations:", error));
}

function capitalizeEachWord(string) {
    return string.split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase()).join(' ');
}

function changePage(direction) {
    currentPage += direction;
    performSearch();
}

function clearSearch() {
    currentFilter = "";
    currentSearchAttribute = "name";
    currentSearchValue = "*";
    currentPage = 0;

    // Ripristina l'interfaccia utente
    document.getElementById("searchInput").value = ""; // Pulisce la barra di ricerca
    document.getElementById("attribute").value = "name"; // Resetta l'attributo selezionato
    performSearch();
}

// Funzione per filtrare per lettera
function filterByLetter(letter) {
    currentFilter = letter; // Salva il filtro alfabetico selezionato
    currentPage = 0; // Resetta alla prima pagina
    performSearch();
}


// EVENT LISTENER

document.getElementById("searchButton").addEventListener("click", () => {
    currentSearchAttribute = document.getElementById("attribute").value || "name";
    currentSearchValue = document.getElementById("searchInput").value || "*";
    currentFilter = ""; // Resetta il filtro alfabetico
    currentPage = 0; // Resetta alla prima pagina
    performSearch();
});

document.getElementById("searchInput").addEventListener("keydown", function (event) {
    if (event.key === "Enter") {
        currentSearchAttribute = document.getElementById("attribute").value || "name";
        currentSearchValue = document.getElementById("searchInput").value || "*";
        currentFilter = ""; // Resetta il filtro alfabetico
        currentPage = 0; // Resetta alla prima pagina
        performSearch();
    }
});

// Esegui una ricerca iniziale quando la pagina viene caricata
window.onload = function () {
    performSearch();
};




import scrapy
import json






##### STOCKS FOR ITALY ( THE SITE THAT WE WERE PROVIDED ) #####


class StocksSpider(scrapy.Spider):
    name = 'stocks'
    allowed_domains = ['borsaitaliana.it']

    start_urls = [
        f'https://www.borsaitaliana.it/borsa/azioni/listino-a-z.html?initial={chr(i)}&lang=en'
        for i in range(ord('A'), ord('Z') + 1)
    ]

    def __init__(self):
        self.results = []

    def parse(self, response):
        all_tr = response.css('tr')
        for tr in all_tr:
            name = [item.strip() for item in tr.css('a .t-text::text').extract() if item.strip()]
            last = [item.strip() for item in tr.css('td:nth-child(2) .t-text::text').extract() if item.strip()]
            percentage = [item.strip() for item in tr.css('.-xs:nth-child(3) .t-text::text').extract() if item.strip()]
            time = [item.strip() for item in tr.css('.-xs:nth-child(4) .t-text::text').extract() if item.strip()]
            low = [item.strip() for item in tr.css('.-xs:nth-child(5) .t-text::text').extract() if item.strip()]
            high = [item.strip() for item in tr.css('.-xs:nth-child(6) .t-text::text').extract() if item.strip()]
            opening = [item.strip() for item in tr.css('.-xs:nth-child(7) .t-text::text').extract() if item.strip()]

            if any([name, last, percentage, time, low, high, opening]):
                self.results.append({
                    'name': name[0] if name else "",
                    'last': last[0] if last else "",
                    'percentage': percentage[0] if percentage else "",
                    'time': time[0] if time else "",
                    'low': low[0] if low else "",
                    'high': high[0] if high else "",
                    'opening': opening[0] if opening else "",
                })

    def closed(self, reason):
        sorted_results = sorted(self.results, key=lambda x: x['name'].lower() if x['name'] else "")
        output_file = 'stocks.json'
        with open(output_file, 'w') as f:
            json.dump(sorted_results, f, indent=4)

        self.log(f"Saved sorted results to {output_file}")







##### TRADINGVIEW SITE OF THE TOP GAINERS #####

class FinanceSpider(scrapy.Spider):
    name = 'stocks2'
    allowed_domains = ['tradingview.com']
    start_urls = [
        'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/'
    ]

    def __init__(self):
        self.results = []

    def parse(self, response):
        rows = response.css('tr')

        for row in rows:
            Name = row.css('.tickerDescription-GrtoTeat::text').get()
            Price = row.css('.right-RLhfr_y4:nth-child(3)::text').get()
            Volume = row.css('.right-RLhfr_y4:nth-child(4)::text').get()
            Market_gap = row.css('.right-RLhfr_y4:nth-child(6)::text').get()

            if Name or Price or Volume or Market_gap:
                self.results.append({
                    'Name': Name if Name else "",
                    'Price': Price if Price else "",
                    'Volume': Volume if Volume else "",
                    'Market_gap': Market_gap if Market_gap else "",
                })

    def closed(self, reason):
        sorted_results = sorted(self.results, key=lambda x: x['Name'].lower() if x['Name'] else "")
        output_file = 'stocks2.json'
        with open(output_file, 'w') as f:
            json.dump(sorted_results, f, indent=4)

        self.log(f"Saved sorted results to {output_file}")





#####  FRENCH ACTIONS #####

class FranciaSpider(scrapy.Spider):
    name = 'stocks3'
    allowed_domains = ['trading.sat']

    start_urls = [
        f'https://www.tradingsat.com/actions-de-a-z/archives-{pg}.html?o=a&f=n&m='
        for pg in range(1, 7)
    ]

    def __init__(self):
        self.results = []

    def parse(self, response):
        cols = response.css('tr')
        for col in cols:
            Name = col.css('.desc .link::text').get()
            High = col.css('.text-right:nth-child(6)::text').get()
            Low = col.css('td:nth-child(7)::text').get()
            Volume = col.css('.text-right:nth-child(8)::text').get()

            if Name or High or Low or Volume:
                self.results.append({
                    'Name': Name if Name else "",
                    'High': High if High else "",
                    'Low': Low if Low else "",
                    'Volume': Volume if Volume else "",
                })

    def closed(self, reason):
        sorted_results = sorted(self.results, key=lambda x: x['Name'].lower() if x['Name'] else "")
        output_file = 'stocks3.json'
        with open(output_file, 'w') as f:
            json.dump(sorted_results, f, indent=4)

        self.log(f"Saved sorted results to {output_file}")
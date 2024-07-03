import requests
from bs4 import BeautifulSoup
import time

def get_quotes_from_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='quote')

    quotes = []
    for quote in quote_elements:
        text = quote.find('div', class_='quoteText').get_text()
        author = quote.find('span', class_='authorOrTitle').get_text()
        quotes.append(f"{text}) - {author}")

    return quotes


def scrape_quotes(base_url, max_pages=100):
    all_quotes = []
    page_num = 1

    while len(all_quotes) < max_pages * 10:
        url = f"{base_url}?page={page_num}/"
        quotes = get_quotes_from_page(url)
        if not quotes:
            break

        all_quotes.extend(quotes)
        print(f'Finished scraping page {page_num}')
        page_num += 1
        time.sleep(1)

    return all_quotes[:max_pages * 10]

def main():
    # Goodreads popular quotes landing page
    quotes_url = 'https://www.goodreads.com/quotes'

    # Scrape up to 3000 quotes (100 pages)
    quotes = scrape_quotes(quotes_url, max_pages=100)

    # Save the quotes to a file
    with open('quotes2.txt', 'w') as file:
        for quote in quotes:
            file.write(f"{quote}\n")

    print(f"Scraped {len(quotes)} quotes.")

if __name__ == "__main__":
    main()

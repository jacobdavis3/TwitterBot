import requests
from bs4 import BeautifulSoup
import time


def get_quotes_from_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve page: {url}")
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    quote_elements = soup.find_all('div', class_='quote')

    quotes = []
    for quote in quote_elements:
        text = quote.find('div', class_='quoteText').get_text(strip=True)
        if len(text) <= 277:
            quotes.append(f"{text}")

    return quotes

def scrape_quotes(base_url, max_pages=2000):
    all_quotes = []
    page_num = 1

    while len(all_quotes) < max_pages * 50:  # Counted 30 quotes per page
        url = f"{base_url}?page={page_num}/"
        quotes = get_quotes_from_page(url)
        if not quotes:
            break

        all_quotes.extend(quotes)
        print(f'Finished scraping page {page_num}')
        page_num += 1
        time.sleep(3)  # Not hammering server

    return all_quotes[:max_pages * 50]  # Limit to the desired number of quotes

def main():
    print('Going to sleep for 20 secs')
    time.sleep(20)
    print('Starting to scrape')
    # Goodreads popular quotes landing page
    # https://www.goodreads.com/quotes?page=1
    quotes_url = 'https://www.goodreads.com/quotes'

    # Scrape up to 3000 quotes (100 pages)
    quotes = scrape_quotes(quotes_url, max_pages=2000)

    # Save the quotes to a file
    with open('quotes2.txt', 'w') as file:
        for quote in quotes:
            file.write(f"{quote}\n")

    print(f"Scraped {len(quotes)} quotes.")

if __name__ == "__main__":
    main()


    
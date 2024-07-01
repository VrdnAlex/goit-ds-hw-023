import requests
from bs4 import BeautifulSoup
import json

url = 'http://quotes.toscrape.com'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')


def get_author_details(author_url):
    response = requests.get(author_url)
    soup = BeautifulSoup(response.text, "lxml")
    fullname = soup.find("h3", class_="author-title").get_text().strip()
    born_date = soup.find("span", class_="author-born-date").get_text().strip()
    born_location = soup.find("span", class_="author-born-location").get_text().strip()
    description = soup.find("div", class_="author-description").get_text().strip()

    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }


def scrape_quotes(base_url):
    quotes = []
    authors = {}
    page = 1

    while True:
        response = requests.get(f"{base_url}/page/{page}/")
        soup = BeautifulSoup(response.text, "lxml")
        quote_elements = soup.find_all("div", class_="quote")

        if not quote_elements:
            break

        for quote_element in quote_elements:
            text = quote_element.find("span", class_="text").get_text()
            author_name = quote_element.find("small", class_="author").get_text()
            tags = [tag.get_text() for tag in quote_element.find_all("a", class_="tag")]
            quotes.append({"quote": text, "author": author_name, "tags": tags})

            author_url = base_url + quote_element.find("a")["href"]
            if author_name not in authors:
                authors[author_name] = get_author_details(author_url)

        page += 1

    return quotes, list(authors.values())


def save_to_json(filename, data):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


base_url = "http://quotes.toscrape.com"
quotes, authors = scrape_quotes(base_url)
save_to_json("quotes.json", quotes)
save_to_json("authors.json", authors)

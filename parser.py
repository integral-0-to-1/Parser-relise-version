import requests
from bs4 import BeautifulSoup as BS

__HOST = "http://www.bing.com/search?q="
__HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36'
}


def get_html(url, params=''):
    r = requests.get(__HOST + url, headers=__HEADERS, params=params)
    return r


def get_content(html) -> list:
    soup = BS(html, 'html.parser')
    items = soup.find_all("li", class_="b_algo")
    results = []
    for item in items:
        results.append(
            {
                "title": item.find("h2").find("a").get_text(strip=True),
                "link": item.find("h2").find("a").get("href")
            }
        )
    print(type(results))
    return results


def get_text(links: list) -> list:
    text_in_pages = []
    for page in links:
        soup = BS(get_html(page["link"]).content, 'html.parser')
        article = soup.select("body")[0].get_text()
        text_in_pages.append(
            {
                "title": page["title"],
                "link": page["link"],
                "text": article
            }
        )

    return text_in_pages


def relevance(text_in_pages: list, search_request: str) -> list:
    keywords = search_request.split(" ")
    site_rating = []
    for page in text_in_pages:
        coincidence_counter = 0
        for keyword in keywords:
            if keyword in page["text"]:
                coincidence_counter += page["text"].count(keyword)
        site_rating.append(
            {
                "title": page["title"],
                "link": page["link"],
                "personal_rating": coincidence_counter
            }
        )

    return site_rating


def choice_best(site_rating: list) -> dict:
    best_site = site_rating[0]

    for site in site_rating:
        if site["personal_rating"] > best_site["personal_rating"]:
            best_site = site

    return best_site

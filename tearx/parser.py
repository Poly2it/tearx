from bs4 import BeautifulSoup

from content_classes import QueryPage, GeneralArticle, GeneralMeta

def parse_response(response):
    categories = {
        'category_general': 'general',
        'category_images': 'images',
        'category_videos': 'videos',
        'category_news': 'news',
        'category_map': 'map',
        'category_music': 'music',
        'category_it': 'it',
        'category_science': 'science',
        'category_files': 'files',
        'category_social media': 'social_media'
    }

    soup = BeautifulSoup(response, 'html.parser')

    xml_articles = soup.find_all("article", {"class": "result"})
    xml_filters = soup.find("div", {"class": "search_filters"})

    category = categories[soup.find("div", {"id": "categories"}).find("input", {"checked": "checked"}).get('name', [])]

    articles = []
    if category == 'general':
        for article in xml_articles:
            classes = article.get('class', [])

            engines = [c for c in classes if c not in ['result', 'result-default', 'category-general']]

            articles.append(GeneralArticle(
                article.h3.text,
                article.h3.a.get('href'),
                article.p.get_text(strip = True),
                engines
            ))

            # result count doesn't always show for some reason
            try:
                result_count = soup.find("p", {"id": "result_count"}).find("small").text.split(":")[1].strip().replace(",", "")
            except:
                result_count = -1

            meta = GeneralMeta(
                result_count = result_count
            )

    query = soup.find("input", {"id": "q"}).get('value', [])
    language = xml_filters.find("select", {"id": "language"}).find("option", {"selected": "selected"}).get('value', [])
    safesearch = xml_filters.find("select", {"id": "safesearch"}).find("option", {"selected": "selected"}).get('value', [])
    
    return QueryPage(
        query,
        language,
        safesearch,
        category,
        meta,
        articles
    )
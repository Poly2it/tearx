import json

from dataclasses import dataclass

@dataclass
class Article:
    title: str
    url: str
    content: str
    engines: list[str]

    @classmethod
    def from_json(cls, article_dict):
        return cls(**article_dict)
        
@dataclass
class QueryPage:
    query: str
    language: str
    safesearch: int
    result_count: int
    category: str
    articles: list[Article]

    def dump(self):
        articles_json = [article.__dict__ for article in self.articles]
        data = {
            "query": self.query,
            "language": self.language,
            "safesearch": self.safesearch,
            "result_count": self.result_count,
            "category": self.category,
            "articles": articles_json
        }
        return json.dumps(data, separators=(',', ':'))

    @classmethod
    def from_json(cls, json_data):
        querypage_dict = json.loads(json_data)
        articles = [Article.from_json(article_json) for article_json in querypage_dict['articles']]
        querypage_dict['articles'] = articles
        return cls(**querypage_dict)
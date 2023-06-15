import json

from dataclasses import dataclass

from typing import Union

@dataclass
class GeneralArticle:
    title: str
    url: str
    description: str
    engines: list[str]

    @classmethod
    def build(self, source):
        return GeneralArticle(
            title = source['title'],
            url = source['url'],
            description = source['description'],
            engines = source['engines']
        )

    def export(self):
        return {
            "title": self.title,
            "url": self.url,
            "description": self.description,
            "engines": self.engines
        }

@dataclass
class GeneralMeta:
    result_count: int

    @classmethod
    def build(self, source):
        return GeneralMeta(
            result_count = source['result_count']
        )

    def export(self):
        return {
            "result_count": self.result_count
        }

@dataclass
class QueryPage:
    query: str
    language: str
    safesearch: int
    category: str
    meta: Union[GeneralMeta]
    articles: list[Union[GeneralArticle]]

    @classmethod
    def build(self, source):
        # load source with json.loads(json_data)
        if source['category'] == 'general':
            articles = [GeneralArticle.build(article) for article in source['articles']]
            
            meta = GeneralMeta.build(source['meta'])

        return QueryPage(
            query = source['query'],
            language = source['language'],
            safesearch = source['safesearch'],
            category = source['category'],
            meta = meta,
            articles = articles
        )

    def export(self):
        articles_export = [article.export() for article in self.articles]
        meta_export = self.meta.export()
        data = {
            "query": self.query,
            "language": self.language,
            "safesearch": self.safesearch,
            "category": self.category,
            "meta": meta_export,
            "articles": articles_export
        }
        return json.dumps(data, separators=(',', ':'))
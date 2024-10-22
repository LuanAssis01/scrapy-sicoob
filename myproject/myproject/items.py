import scrapy # type: ignore

class ArticleItem(scrapy.Item):
    title_article = scrapy.Field()   # Título do artigo
    resumo_article = scrapy.Field()  # Resumo do artigo
    image = scrapy.Field()           # Imagem do artigo
    text = scrapy.Field()            # Texto completo do artigo

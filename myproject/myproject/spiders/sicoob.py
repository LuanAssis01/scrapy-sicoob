import scrapy # type: ignore
from myproject.items import ArticleItem
from urllib.parse import urljoin

class SicoobSpider(scrapy.Spider):
    name = "sicoob"
    start_urls = ["https://www.sicoob.com.br/web/maisqueumaescolha/blog/-/blogs/"]
    
    def parse(self, response):
        # Iterar sobre os posts do blog
        for article in response.css(".widget-mode-simple"):
            title = article.css('.title-link::text').getall()
            summary = article.css('.widget-content p::text').getall()
            image = article.css('.widget-content').getall()

            # Imprimir os dados para depuração
            print("Título:", title)
            print("Resumo:", summary)
            print("Imagem:", image)

            # Se o título e resumo forem encontrados, yield os dados
            yield {
                    'titulo': title,
                    'resumo': summary,
                    'imagem': image
                }

            # Seguir o link do artigo para coletar mais informações
            article_link = article.css('.title-link::attr(href)').get()
            if article_link:
                yield response.follow(article_link, self.parse_article)

        # Paginação - Seguir para a próxima página, se existir
        next_page = response.css('.pagination-bar ul.pagination li.page-item a.page-link::attr(href)').getall()

        for next in next_page:
            if next and not next.startswith('javascript:;'):
                # Garantir que a URL da página seja válida
                next_page_url = urljoin(response.url, next)
                # print(f"Seguindo para a próxima página: {next_page_url}")  # Debug para verificar a URL
                # Seguir para a próxima página chamando a própria função 'parse'
                yield response.follow(next_page_url, self.parse)

            
    def parse_article(self, response):

        titulo_completo = response.css('.container .widget-mode-detail-header h3::text').getall()  # Título do artigo completo
        texto_completo = response.css('.container .widget-mode-detail-header p::text').getall()  # Texto completo

        yield {
                'titulo_completo': titulo_completo,
                'texto_completo': texto_completo
        }


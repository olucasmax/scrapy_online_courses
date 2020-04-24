import scrapy

class UdacityBaseSpider(scrapy.Spider):
    name = "Udacity"
  
    start_urls = ['https://pt-br.classpert.com/search?filter%5Bprovider_name%5D%5B%5D=Udacity&filter%5Bprice%5D%5B%5D=0&filter%5Bprice%5D%5B%5D=2500&p=1&q=python']
    
    def parse(self,response):
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.113 Safari/537.36'}

        path = response.css('#results > div:nth-child(2) > div ~ div > div > div > div:nth-child(3) > div:nth-child(2) > a::attr(href)').extract()    
        for next_course in path:
            link_curso = response.urljoin(next_course)
            yield scrapy.Request(link_curso, callback=self.parse_cursos,encoding='utf-8')

            
    def parse_cursos(self, response):
        
        labels = response.css('div.col-4 > div > div')

        xp = response.xpath('/html/body/div[3]/div/div[1]')
        sub_price = xp.css('div.el\:amx-Bc_su.el\:amx-Pt\(1\.5em\).el\:amx-Pb\(2\.5em\) > div > div > div.col-3.el\:amx-D\(f\) > div > div > div.el\:amx-D\(f\).el\:amx-FxDi\(c\).el\:amx-FxAi\(fe\).el\:amx-FxJc\(c\) > div > span > span::text').get()
        
        str(sub_price).strip()
        price = ('Free' if (sub_price is None) else sub_price)
        
        yield {
        'course_name' : response.css('div.el\:m-text-clipbox > a::text').extract_first().strip(),
        'audio'       : labels.css('div:nth-child(1) > span > span > span::text').extract_first().strip(),
        'subtitles'   : labels.css('div:nth-child(2) > span > span > span::text').extract_first().strip(),
        #'instructor_name' : labels.css('div:nth-child(3) > span > span::text').extract_first().strip(),
        #'ritm_desc'   : labels.css('div:nth-child(4) > span > span::text').extract_first().strip(),
        #'level'       : labels.css('div:nth-child(5) > span > span::text').extract_first().strip(),
        #'workload'    : labels.css('div:nth-child(6) > span > span::text').extract_first().strip(),
        'description' : response.css('div.col-8 > div > div:nth-child(1) p::text').extract_first(),
        'price'       : price
        }
        
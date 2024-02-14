import scrapy
import re
import hashlib
from ..items import JobfinderItem 
from scrapy_splash import SplashRequest 
from scrapy.exceptions import CloseSpider
import pathlib
import configparser


class JobdnesSpider(scrapy.Spider):
    name = "jobdnes"
    allowed_domains = ["www.jobdnes.cz"]
    current_page = 0
    total_page_num = None

    @classmethod
    # Loading desired key word to scrape from the configuration file - scrapy.cfg.
    def load_config_data(cls):
        config = configparser.ConfigParser()
        config.read(pathlib.Path(__file__).parent.parent.parent.joinpath('scrapy.cfg').resolve())
        return config['spider']['key_word']
    
    def __init__(self):
        self.key_word = self.load_config_data()
        # Initiating Splash script which loads home page, type desired key word into search field and submit
        # Script returns url and html of searched result
        self.init_script = '''
        function main(splash, args)
          splash:set_user_agent('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203')
          assert(splash:go(args.url))
          assert(splash:wait(0.5))
          local btn = splash:select("#didomi-notice-agree-button")
          if btn then
            splash:select("#didomi-notice-agree-button").mouse_click()
          else
          end
          splash:wait(0.5)
          inpt = splash:select(".std-form input")
          inpt:focus()
          inpt:send_text("{key}")
          splash:wait(0.5)
          splash:send_keys("<Enter>")
          splash:wait(0.5)
          splash:send_keys("<Enter>")
          splash:wait(10)
          splash:set_viewport_full()
          splash:wait(2)
          return {{ html = splash:html(),url=splash:url() }}
        end
    
        '''.format(key=self.key_word)
        
    def start_requests(self):
        # initial request to jobdnes.cz via Splash 
        yield SplashRequest(url = "https://www.jobdnes.cz",callback=self.parse_init,endpoint="execute",args={"lua_source":self.init_script}) 

    def parse_init(self,response):
        # print(response.headers.get('Content-Type'))
        # Checking if any results returned
        no_results_found = response.xpath("//div[contains(@class,'alert-error')]").get()
        if no_results_found:
            raise CloseSpider("No Match")
        else:
            print(f'Results found for the position: {self.key_word}')
            pass
        # Pagination
        page_nav = response.xpath('//div[@class="paginator"]/span[@class="paginator-group"][last()]/span[last()]/@class').get()
        if page_nav: 
            self.total_page_num = int(re.search(f"\d+",page_nav).group())
        else:
            self.total_page_num = 0
        return self.parse(response)
    
    def parse(self, response):
        item = JobfinderItem()
        #get all offers from current page
        list_of_offers = response.xpath('//div[@class="list-offers"]//div[@class="entry " ]')
        #iteration over page's offers 
        for offer in list_of_offers:
            item["portal"] = "jobDNES.cz"
            item['searched_position'] = self.key_word
            item["position_name"] = offer.xpath(".//h3/a/text()").get()
            item["company"] = self.company_finder(offer)
            item["location"] = offer.xpath('.//*[@class="place"]/a/text()').get()
            list_of_texts = offer.xpath(".//p/text()").getall()
            wage = list(filter(lambda x: re.search(r"(měsíc|hodina|hodinu)",x),list_of_texts))
            item["wage"] = wage[0] if wage else ""
            position_link_relative = offer.xpath('.//h3/a/@href').get() 
            item["link"] = response.urljoin(position_link_relative)      
            item['id'] = hashlib.sha1(item['link'].encode()).hexdigest()
            item["page"] = self.current_page
            yield item
        #if not last web page go to another
        if self.current_page < self.total_page_num:
            self.current_page += 1
            next_url = response.xpath(f"//span[contains(@class,'paginator-page-{self.current_page}')]/a/@href").get()
            yield response.follow(url = next_url,callback=self.parse)

    def company_finder(self,offer):
        #finding company name 
        list_of_classes = ['.//*[@class="company"]/a/text()','.//*[@class="name"]/text()'] #css classes where company name might be listed
        for item_class in list_of_classes:
            cur_item = offer.xpath(item_class).get()
            if cur_item:
                return cur_item
            else:
                pass
        return None










import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst
from w3lib.html import remove_tags
import os

#using Scrapy Python For Web Crawler 
# Removing tags spaces and empty string
def remove_white_space(value):
    return value.strip().replace("\n", "")
#For Tags removing we will use w3lib.html 
#Before fetching items we will remove tags whitespaces Make Order like Name Price Ratings and URL
class Product(scrapy.Item):
    name= scrapy.Field(input_processor = MapCompose(remove_tags, remove_white_space), output_processor = TakeFirst())
    price = scrapy.Field(input_processor = MapCompose(remove_tags, remove_white_space), output_processor = TakeFirst())
    ratings = scrapy.Field(input_processor = MapCompose(remove_tags, remove_white_space), output_processor = TakeFirst())
    url = scrapy.Field()
#Common Practices of Scrapy we will use this class
class BananaSpider(scrapy.Spider):
    name = "banana_spider"
    #before starting requests lets check url proxy and parse HTML , XML etc items
    def start_requests(self):
         urls = ["https://bananafingers.com/climbing-holds"]
         for url in urls:
             yield scrapy.Request(url=url,  meta = {"proxy": os.getenv("proxy")},callback=self.parse_item)
    #After Requests lets Handle Response 
    #in Response the Basic get reponse.css("tag.classname") is inseted 
    #Through Help of Itemloader which is also Scrappy Loader we will Load all the Items in the Product
    #then Copy the Class and Tag name from Inspect element of the Site and paste in 
    #add_css Itemloader will handle the response of the items in the response.css
    #and check for the Name Tag and Price tag and URL value from url and their respective classes 
    #then all the items will be yield in loaditem class
    def parse_item(self,response):
        for item in response.css("div.product-item-info"):
            il = ItemLoader(item=Product(), selector=item)
            il.add_css("name","a.product-item-link")
            il.add_css("price","span.price")
            il.add_value("url",response.url)
            yield il.load_item()
#Checking 2 Other Websites 
class EliteMountainSpider(scrapy.Spider):
    name = "FoodEliteMountain_spider"
    
    def start_requests(self):
         urls = ["https://www.elitemountainsupplies.co.uk/camping-trekking-c4/eating-c20/food-c81"]
         for url in urls:
             yield scrapy.Request(url=url,  meta = {"proxy": os.getenv("proxy")},callback=self.parse_item)
    def parse_item(self,response):
        for item in response.css("div.product__details__holder"):
            il = ItemLoader(item=Product(), selector=item)
            il.add_css("name","a.infclick")
            il.add_css("price","span.GBP")
            il.add_value("url",response.url)
            yield il.load_item()

class Needlewear(scrapy.Spider):
    name = "Needle_spider"
    
    def start_requests(self):
         urls = ["https://www.needlesports.com/Catalogue/Clothing-Footwear/Crag-Clothing/T-Shirts"]
         for url in urls:
             yield scrapy.Request(url=url,  meta = {"proxy": os.getenv("proxy")},callback=self.parse_item)
    def parse_item(self,response):
        for item in response.css("div.NamePriceWrap"):
            il = ItemLoader(item=Product(), selector=item)
            il.add_css("name","div.Name")
            il.add_css("price","div.Price")
            il.add_value("url",response.url)
            yield il.load_item()
#Simple Common Practices Scrappy Documentation format
#link: https://docs.scrapy.org/en/latest/topics/practices.html
process = CrawlerProcess(
    settings={
        "FEEDS": {
            #FORMAT CSV File
           "results.csv":{"format":"csv"},
        },
        #Defining User Agent utf format Fingerprint Async Functions Robotstxt Verification for Allowed or not allowed 
        "USER_AGENT":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "REQUEST_FINGERPRINTER_IMPLEMENTATION":"2.7",
        "FEED_EXPORT_ENCODING":"utf-8",
        "DNS_TIMEOUT": 120,
        "ROBOTSTXT_OBEY": False,
        "TWISTED_REACTOR":"twisted.internet.asyncioreactor.AsyncioSelectorReactor",
    }
)
#First Check the Crawler Process and than Check dependances than Crawl...... 
#Websites like Amazon Daraz Nike were tested but due to 403 Error Crawler cannot crawl to fetch data 
#These Three Websites are Taken which can be tested later on
process.crawl(BananaSpider)
process.crawl(EliteMountainSpider)
process.crawl(Needlewear)
process.start()

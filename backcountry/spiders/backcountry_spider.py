import scrapy
import json
import re
class BackcountrySpiderSpider(scrapy.Spider):
    name = 'backcountry_spider'
    
    custom_settings = {
		'FEEDS': {
			'backcountry.csv': {
				'format': 'csv',
				'encoding': 'utf-8-sig',
				'overwrite': True,
			},
		},
	}
    
  
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'priority': 'u=0, i',
        'referer': 'https://www.backcountry.com/snowboard-bags',
        'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Google Chrome";v="126"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36',
    }

    
    
    def start_requests(self):
     
        url='https://www.backcountry.com/productSitemap.xml'
        yield scrapy.Request(url=url, callback=self.get_products_links,headers=self.headers)

    def get_products_links(self,response):
        
        
        links=re.findall('loc>([^<]+)<',response.text)
 
        for link in links:
            yield scrapy.Request(url=link, callback=self.scrape_product_page,headers=self.headers)
    
    def scrape_product_page(self, response):
        data = response.xpath("//script[@type='application/ld+json'][contains(text(),'ProductGroup')]/text()").get()
        
        if data:
            product_info = json.loads(data)
            product_name = product_info.get('name')
            product_description = response.xpath('//div[@data-id="productDetailsSection"]//p/text()').get()
            product_sku = product_info.get('sku')
            product_category = product_info.get('category')
            product_material = product_info.get('material')
            product_brand = product_info.get('brand', {}).get('name')
            product_colors = product_info.get('color', [])
            product_images = product_info.get('image', [])
            aggregate_rating = product_info.get('aggregateRating', {}).get('ratingValue')

            variants_list = []
            tech_dic={}
            techs=response.xpath('//div[@data-id="techSpecsSection"]//div[@class="css-37f4v5"]')
            for tech in techs:
                key=tech.xpath('.//dt/text()').get()
                value=tech.xpath('.//dd/text()').get()
                tech_dic[key]=value

            for variant in product_info.get('hasVariant', []):
                variant_details = {
                    'name': product_name,
                    'description': product_description,
                    'sku': product_sku,
                    'category': product_category,
                    'material': product_material,
                    'brand': product_brand,
                    'color': variant.get('color'),
                    'size': variant.get('size'),
                    'variant_sku': variant.get('sku'),
                    'price': variant.get('offers', {}).get('price'),
                    'currency': variant.get('offers', {}).get('priceCurrency'),
                    'availability': variant.get('offers', {}).get('availability'),
                    'condition': variant.get('offers', {}).get('itemCondition'),
                    'seller': variant.get('offers', {}).get('seller', {}).get('name'),
                    'aggregate_rating': aggregate_rating,
                    "techs":tech_dic,
                    "product_url":response.url
                }
                variants_list.append(variant_details)

         
            for variant in variants_list:
                yield variant

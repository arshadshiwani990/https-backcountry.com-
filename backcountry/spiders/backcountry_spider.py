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
        # 'cookie': 'optimizelyEndUserId=oeu1720310826177r0.6572174761501401; _abck=EE12FB8487BBFD6356BD9577DFFE1720~0~YAAQ1TB7XGkFNnWQAQAA8AqEigwnIw/EB716ja/2Z9zbNWqvLu1FUdloH9dIXbfYCZbIWH7KJtMa/8vKn3k3Y3cSBK4+i9hX2r7rnci0n3umiY0GjCjdUbGzK1YFI7ZOYM1FbsGWx4LSR1Rh4L9slRt1aw+P8mG4KRDpnRAJ+RH786ai1KnR0PbNEDm7/oiIgaCRxBZAZqeSBnrCKmFSwUvZkTTAb32htxP8MvDArjBcdrfuMHxE/eRDik5Fj8qW3YkLdSpBTuz1Su1E0rUvJiKk7hBcbpGqvUQQcNUe0ZuMTNDTaRGILfD4e0+4ADmRdLjGwIDKhvGvsngkoYQwWbIawo7jhz3t31y3bBsGZ8YFMbqC9yO/GajqEYlva6nDSKAkyTK9Pq2PxXbtRRJ6oSFJx+bB4zryDlESwi8=~-1~||0||~1720314427; _gcl_au=1.1.1441427400.1720310826; ak_bmsc=84BD0C4DE7E862BBEDC18F5337630B26~000000000000000000000000000000~YAAQ1TB7XH8FNnWQAQAANxKEihiLe7cZ5uZediRNhgVUn1TuJW7BhD8G+egeFsJBZocJn0mJyZv9EZl85GDxmE0NgpEu4FpUtSXou/hkP4ASJwt8e+HJbNmgOjmYc8tuIsFcw/rrVSQ4ZPfXUhxuN6GFYp303s4y/8+JkOueQPzUcGCOv1vw2uUCMerxtumxBawp+LJnsyFUauuudf2oouiUT2HdlNrtJ1nJZrjfBUGljS576QM9h4Jd0tUE/MWb+JPE7NnQvcyka2PzddfpBem8P0I+OyjB1o+RdsVukvwBc8WhVhI3tmnIuKDz8eOlNTlqyadfSIbnBIC/Rc16PGLkOcx3iua8IGIqNcbGdAencIY6ISdONS0i0coJFTAygUcTwCQ+/sYrbb/agPlIGpgkf2oESSvwvUpiC+DTaEEl6oJFBTLmpjD3k3uM5+t5DNte+FeF6iLrPDM1M5EJAQ==; _gid=GA1.2.1080332782.1720310830; IR_gbd=backcountry.com; _sp_ses.f192=*; rmStore=dmid:false; _fbp=fb.1.1720310834384.738722599852828940; v2_backcountry={%22bid%22:%22e407061b-481a-494c-9782-a07d39d601a2%22}; IR_PI=df5ede78-3bf4-11ef-9275-a178ed13f299%7C1720310833997; _clck=1x6a9fo%7C2%7Cfn9%7C0%7C1649; OptanonAlertBoxClosed=2024-07-07T00:07:16.050Z; __attentive_id=cb9399a2cdce4fb3b61b1bd867396a2c; _attn_=eyJ1Ijoie1wiY29cIjoxNzIwMzEwODM3OTkyLFwidW9cIjoxNzIwMzEwODM3OTkyLFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcImNiOTM5OWEyY2RjZTRmYjNiNjFiMWJkODY3Mzk2YTJjXCJ9In0=; __attentive_cco=1720310837995; __attentive_dv=1; __attentive_ss_referrer=ORGANIC; AKA_A2=A; unbxd.userId=uid-1720310844543-71191; unbxd.visit=first_time; unbxd.visitId=visitId-1720310844547-90216; __attentive_domain=backcountry; __attentive_ceid=iVG; mdLogger=false; kampyle_userid=5a01-7c78-ceb5-fce6-4e93-47da-b24b-d2a9; BVBRANDID=e401978a-6dd8-4301-ac2a-edf210412176; BVBRANDSID=36ce2546-9cc2-4612-85c4-02cc0978a7ef; bm_sz=E8ED7E9015E3B4023C2A18E0B04CF03C~YAAQ1TB7XL0VNnWQAQAAGZ6IihgcCX/LhYUVP4C2GkRB4ce+B2lcrkAaY3f/jZDIQ0oFrSDjbo8s+TK6+AvH0Ueu/PuLm9PzgSIfTq/o03qPGi2PdD7D5EE63dDoUU0eWQ+LqLzNWnTIZnimsHBbUmPVvaQWh5JWXoMemOG60Sd5OLjcQ5oJ+6Kj/reMqL6bekT1xMKouEPimIOBlzWj2QIFngG3lv3FXyp1ac0GiyDSeQfvyIc3MOO23x3eEhALM3Vw2GaM4BwVE0+hR0Lp0yqYQ/+LczDOj1C3TmZSAXgMmpVQ8O/+BDUVZjYF8JbjrMgMLFiamsx1RVh0cf1qhznRKfhsQKAqeTcyyj+NYbRIvJvc0OXW9pdCFxa3GqhsLBOxmxhANCiuBiUlqCYZxVoUpDuYkHuaBAHWsxUGxuSVGAawKl1m6jw26lkG1ceeOcsXoFOu~3488056~4600133; bm_sv=D796EF36952F48CE7263470CA04186B9~YAAQ1TB7XNwVNnWQAQAA+qWIihiUQTThBkhgnxCmRG+pTnNVSaX1dycdQuxe4MCWblbb23alZaoS1EZutNLwv/EFQYQxxS79om0BP40Av015aFj+nxlyQcotFYZSs6fZ8z724HL4WfHZ3kHMBhf1hfAeo34JK+ZDTmT/gr9x8KEYeYRBzMDQbaEAsHNfSaSsD+Un79HkVk3stNymLgkDXZN7vX2/dj5F02XCups3LqsVYEC+fs78oH2RRJqIQSB4er+NU/fz~1; _ga=GA1.2.729315928.1720310829; _sp_id.f192=a0f33236-347b-4d23-8562-5c65f69fb0a0.1720310834.1.1720311129.1720310834.ea43167b-9fe2-442b-aaeb-8b40024ab9fa; da_sid=8B9052FD8FD1AE8B4D89AA13A4DCFC23B8.0|4|0|3; da_lid=B8A361CE9B91EA10D8D8BB99E6DEB6280B|0|0|0; da_intState=; IR_5311=1720311129565%7C0%7C1720311129565%7C%7C; _uetsid=dd5626e03bf411efacaff177324a201c; _uetvid=dd5651303bf411ef81b7090b2ccc19cf; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Jul+07+2024+05%3A12%3A10+GMT%2B0500+(Pakistan+Standard+Time)&version=202208.1.0&isIABGlobal=false&hosts=&consentId=40de7f4d-1bc2-4bc1-aedd-0c7dfb6252ac&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0004%3A1%2CC0003%3A1%2CC0009%3A1&geolocation=PK%3BSD&AwaitingReconsent=false; __attentive_pv=5; _clsk=q3umcq%7C1720311132238%7C5%7C0%7Cx.clarity.ms%2Fcollect; kampyleUserSession=1720311136647; kampyleUserSessionsCount=2; kampyleSessionPageCounter=2; _dc_gtm_UA-29667548-1=1; unbxd.pen.click.1720311324344=eyJwaWQiOiJEQUswMTJXIiwicHIiOiIxIiwicmVxdWVzdElkIjoiMTIzIiwidXJsIjoiaHR0cHM6Ly93d3cuYmFja2NvdW50cnkuY29tL3Nub3dib2FyZC1iYWdzIiwicmVmZXJyZXIiOiJodHRwczovL3d3dy5iYWNrY291bnRyeS5jb20vIiwidmlzaXRfdHlwZSI6ImZpcnN0X3RpbWUiLCJ2ZXIiOiI0LjAuMjgiLCJfdWYiOjIxMzM3MTQwODQsInZpc2l0SWQiOiJ2aXNpdElkLTE3MjAzMTA4NDQ1NDctOTAyMTYifQ%3D%3D; RT="z=1&dm=www.backcountry.com&si=fc5b350b-94a1-4256-bf24-558a1ef8c411&ss=lyasn9om&sl=4&tt=ji2&obo=1&rl=1&nu=4nn6o1qz&cl=arig&ld=arkn&r=1n2an3ki&ul=arko"; _ga_GKCTXSLT4Y=GS1.1.1720310828.1.1.1720311324.53.0.0',
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
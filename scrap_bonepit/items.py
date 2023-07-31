import scrapy
from dataclasses import dataclass


# class ScrapBonepitItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass

@dataclass
class ImageItem:
    patient_id: str
    age_month: int
    is_male: bool
    body_region: str
    image_urls: list[str]
    content_type: str
    images = None

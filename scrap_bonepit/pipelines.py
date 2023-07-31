# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from .items import ImageItem
from scrapy.pipelines.images import ImagesPipeline


class MyImagesPipeline(ImagesPipeline):
    def file_path(self, request, response=None, info=None, *, item: ImageItem = None):
        image_filename = f'{item.body_region}/{item.patient_id}.{item.content_type}'

        return image_filename

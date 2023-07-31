from pathlib import Path
import scrapy
import re
from ..items import ImageItem

_REGEX_AGE_MALE_REGION = re.compile(r'(\d+)m?([MF]) (.+)')


class NormalByAgeSpider(scrapy.Spider):
    name = "normalbyage"

    def start_requests(self):
        urls = [
            "http://bonepit.com/Normal%20for%20age/Normal%20for%20age%20index.htm",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cases_hrefs = response.xpath('//table')[1:].xpath('.//a/@href').getall()
        self.logger.info(f'Found {len(cases_hrefs)} cases in this page.')
        for page_href in cases_hrefs:
            self.logger.info(f'Following Case {page_href}...')
            yield response.follow(page_href,
                                  callback=self.parse_case,
                                  # cb_kwargs=cb_kwargs
                                  )

    @staticmethod
    def _process_metainfos(response):
        casename = response.url.split('/')[-1].split('.')[0].replace('%20', ' ')
        match = _REGEX_AGE_MALE_REGION.match(casename)
        agemonth = int(match[1])
        if 'm' not in casename[:4]:
            agemonth *= 12
        assert match[2] in ['M', 'F']
        metainfos = {'is_male': match[2] == 'M',
                     'body_region': match[3].lower().strip(),
                     'age_month': agemonth,
                     }
        return metainfos, casename

    @staticmethod
    def parse_case(response):
        metainfos, casename = NormalByAgeSpider._process_metainfos(response)
        R = response.xpath('//p[@align="left"]')
        R1 = [r.xpath('./a/@href').getall() for r in R]
        R1 = [r for r in R1 if len(r) > 0]
        R2 = [r.xpath('./img/@src').getall() for r in R]
        R2 = [r for r in R2 if len(r) > 0]
        R = R1+R2
        if len(R) == 0:
            R = [[r] for r in response.xpath('//p/img/@src').getall()]
            assert len(R) > 0
        pid = 0
        for urls in R:
            patient_id = f'{casename}_{pid}'
            assert len(urls) > 0
            for url in urls:
                yield ImageItem(patient_id=patient_id,
                                image_urls=[response.urljoin(url)],
                                content_type=url.split('.')[-1],
                                **metainfos)
            pid += 1

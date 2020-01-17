# -*- coding: utf-8 -*-
import re
import scrapy
import time
from kesenhuang.items import KesenhuangItem

class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['kesen.realtimerendering.com']
    start_urls = ['http://kesen.realtimerendering.com/']
    allowed_confs = ["SIGGRAPH"]

    def parse(self, response):
        group = response.xpath('//div[@id="g_body"]') 
        #conf_names = group.xpath('//h3[count(ancestor::*)<9]/text()').getall()
        conf_names = group.xpath('//h3/text()').getall()
        for idx, conf_name in enumerate(conf_names):
            # if conf_name in self.allowed_confs:
            xpath_string = '//ul[preceding-sibling::h3[1]/text()="{}"]'.format(conf_name)
            conf = group.xpath(xpath_string)
            conf_year_names = conf.xpath('.//li/a/text()').getall()
            conf_year_list = conf.xpath('.//li/a/@href').getall()
            print('conf name: ', conf_name)
            print("year names : ", conf_year_names, conf_year_list)
            for conf_year_name, conf_year in zip(conf_year_names, conf_year_list):
                time.sleep(0.2)
                year = re.findall(r'\d+', conf_year_name)
                if len(year) == 0:
                    continue
                meta = {"conf_name" : conf_name, "conf_year" : year[-1]}
                yield response.follow(conf_year, callback=self.parse_conf, meta=meta)
        pass

    def parse_conf(self, response):
        sec_names = response.xpath('//h2/text()').getall()
        sec_list = response.xpath('//dl')
        for sec_name, sec in zip(sec_names, sec_list):
            paper_titles = sec.xpath('.//dt/b[1]/text()').getall()
            paper_authors = sec.xpath('.//dd')
            for title, author in zip(paper_titles, paper_authors):
                item = KesenhuangItem()
                item["title"] = title
                item["authors"] = author.xpath('.//a/text()').getall()
                item["conference"] = response.meta.get("conf_name")
                item["year"] = response.meta.get("conf_year")
                item["section"] = sec_name
                yield item
        pass

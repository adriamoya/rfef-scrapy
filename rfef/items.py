# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ActaItem(scrapy.Item):
    # define the fields for your item here like:
    urls = scrapy.Field()
    campeonato = scrapy.Field()
    temporada = scrapy.Field()
    jornada = scrapy.Field()
    campo = scrapy.Field()
    arbitros = scrapy.Field()
    fecha = scrapy.Field()
    club_local = scrapy.Field()
    club_visitante = scrapy.Field()
    pass

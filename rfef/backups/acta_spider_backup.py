#!/usr/bin/env python
# -*- coding: latin-1 -*-

import scrapy
import re
import decimal
import datetime
#
from scrapy.conf import settings
from scrapy.spiders import CrawlSpider, Rule
from scrapy.http.request import Request
from scrapy.selector import Selector
#
from ..items import ActaItem

base_url = 'http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100'


# Aux method to return no. of month given the month name
def month_to_number(string):
	months =[
	('enero',1), 
	('febrero',2), 
	('marzo',3),
	('abril',4), 
	('mayo',5),
	('junio',6),
	('julio',7),
	('agosto',8),
	('septiembre',9),
	('octubre',10),
	('noviembre',11),
	('diciembre',12)
	]

	list_months = [month[0] for month in months]
	string_words = string.split()
	month_name = [i for i in string_words if any(month in i for month in list_months)][0]

	for month in months:
		if month[0] == month_name:
			month_number = month[1]

	return month_number




class ActaSpider(scrapy.Spider):
	
	name = 'acta_rfef'	
	allowed_domains = ['actas.rfef.com']
	start_urls = [
		'http://actas.rfef.es/actas/RFEF_CmpJornada?cod_primaria=1000144&CodCategoria=100&CodTemporada=100&CodJornada=1',
	]

	def parse(self, response):

		self.logger.info('SPIDER WORKING ........')

		# self.logger.info(str(response.status))
		# self.logger.info('Parsing page ...')
		# self.logger.info('**************************************')
		
		# for cod_temporada in range(100,114,1):
		# 	for cod_jornada in range(1,38,1):
		cod_temporada = 100
		cod_jornada = 1

		extra_url = '&CodTemporada=%s&CodJornada=%s' % (cod_temporada, cod_jornada)
		page_url = base_url + extra_url

		request = scrapy.Request(
			page_url,
			callback=self.parse_jornada,
			dont_filter=True)

		yield request # request call back from each page

	def parse_jornada(self, response):

		partidos_url = response.xpath('//a/@href').extract()

		for url_raw in partidos_url:
			url = "http://actas.rfef.es" + url_raw.encode('ascii','ignore')
			url_acta1 = url.replace('CmpPartido','CmpActa1')
			url_acta2 = url.replace('CmpPartido','CmpActa2')

			acta = ActaItem()

			acta['urls'] = [url_acta1, url_acta2]

			request = scrapy.Request(
					url_acta1,
					callback=self.parse_acta1,
					dont_filter=True)
			request.meta['item'] = acta

			yield request # request call back from each page



	def parse_acta1(self, response):

		acta = response.meta['item']

		'''
			Row 1:
				- Campeonato
				- Temporada
				- Jornada
			Row 2:
				- Fecha
		'''
		try:
			upper_table = response.xpath('//tr[contains(@class,"BG_TIT_PAG")]')
		except:
			pass

		# Info general

		try:
			temporada = upper_table[0].xpath('.//td/text()').extract()[0].strip().encode('utf-8')
		except:
			pass

		if temporada:
			acta["temporada"] = temporada

		try:	
			campeonato = upper_table[0].xpath('.//td/text()').extract()[1].strip().encode('utf-8')
		except:
			pass

		if campeonato:
			acta["campeonato"] = campeonato

		try:
			jornada = upper_table[0].xpath('.//td/text()').extract()[1].strip().encode('utf-8')
		except:
			pass

		if jornada:
			jornada = int(re.findall('\d+',jornada)[0])
			acta["jornada"] = jornada


		try:
			fecha_dia = int(re.findall('\d+',upper_table[1].xpath('.//td/text()').extract()[0].strip().encode('utf-8'))[0])
			fecha_any = int(re.findall('\d+',upper_table[1].xpath('.//td/text()').extract()[0].strip().encode('utf-8'))[1])
			fecha_mes = int(month_to_number(upper_table[1].xpath('.//td/text()').extract()[0].strip().encode('utf-8')))
		except:
			pass
		
		try:
			hora = response.xpath('//td[contains(text(),"HORA DE COMIENZO")]/ancestor::tr/following-sibling::tr')[2].xpath('./td[contains(text(),"Parte")]/text()').extract()[0].strip().encode('utf-8')
			hora = re.findall('\d+',hora)[-2:]
		except:
			pass

		fecha = datetime.datetime(year=fecha_any, month=fecha_mes, day=fecha_dia, hour=int(hora[0]), minute=int(hora[1]))
		if fecha:
			acta["fecha"] = fecha

		try:
			campo = response.xpath('//td[contains(text(),"Campo:")]/following-sibling::td/text()').extract()[0].strip().encode('utf-8')
		except:
			pass

		if campo:
			acta["campo"] = campo


		# Arbitros

		arbitros = {}

		try:
			arbitros_raw = response.xpath('//td[contains(text(),"Arbitro")]')
			arbitros["arbitro"] = (
				arbitros_raw[0].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8'),
				''.join(re.findall('[^()]',arbitros_raw[0].xpath('./following-sibling::td/text()')[1].extract().strip().encode('utf-8')))
				)

			arbitros["arbitro_asistente_1"] = (
				arbitros_raw[1].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8'),
				''.join(re.findall('[^()]',arbitros_raw[1].xpath('./following-sibling::td/text()')[1].extract().strip().encode('utf-8')))
				)

			arbitros["arbitro_asistente_2"] = (
				arbitros_raw[2].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8'),
				''.join(re.findall('[^()]',arbitros_raw[2].xpath('./following-sibling::td/text()')[1].extract().strip().encode('utf-8')))
				)

			arbitros["cuarto_arbitro"] = (
				arbitros_raw[3].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8'),
				''.join(re.findall('[^()]',arbitros_raw[3].xpath('./following-sibling::td/text()')[1].extract().strip().encode('utf-8')))
				)

			arbitros["delegado"] = (
				response.xpath('//td[contains(text(),"Delegado")]/following-sibling::td/text()').extract()[0].strip().encode('utf-8'),
				''.join(re.findall('[^()]',response.xpath('//td[contains(text(),"Delegado")]/following-sibling::td/text()').extract()[1].strip().encode('utf-8')))
				)	
		except:
			pass

		if arbitros:
			acta["arbitros"] = arbitros

		# Equipo LOCAL

		club = {}

		try:
			# [0] para local, [1] para visitante
			club["nombre"] = ''.join(re.findall('[^EQUIPO:]',response.xpath('//td[contains(text(),"EQUIPO:")]/text()').extract()[0].strip().encode('utf-8'))).strip()
		except:
			pass

		try:
			# Alineaciones: [0] para local, [1] para visitante, Suplentes [2] para local, [3] para visitante
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[0].xpath('./following-sibling::tr/td/text()').extract()
			jugadores_numeros = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(0, len(raw_jugadores),3)]
			jugadores_nombres = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),3)]

			club["alineacion"] = [(jugadores_numeros[i], jugadores_nombres[i]) for i in range(0, len(jugadores_numeros))]

			# Alineaciones: [0] para local, [1] para visitante, Suplentes [2] para local, [3] para visitante
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[2].xpath('./following-sibling::tr/td/text()').extract()
			jugadores_numeros = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(0, len(raw_jugadores),3)]
			jugadores_nombres = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),3)]

			club["suplentes"] = [(jugadores_numeros[i], jugadores_nombres[i]) for i in range(0, len(jugadores_numeros))]
		except:
			pass

		try:
			# [0] para local, [1] para visitante
			club["entrenador"] = response.xpath('//td[contains(text(),"Entrenador")]')[0].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8')

			# [2] para local, [3] para visitante
			club["entrenador_2"] = response.xpath('//td[contains(text(),"Entrenador")]')[2].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8')
		except:
			pass


		acta["club_local"] = club 


		# Equipo VISITANTE

		club = {}

		try:
			# [0] para local, [1] para visitante
			club["nombre"] = ''.join(re.findall('[^EQUIPO:]',response.xpath('//td[contains(text(),"EQUIPO:")]/text()').extract()[1].strip().encode('utf-8'))).strip()
		except:
			pass

		try:
			# Alineaciones: [0] para local, [1] para visitante, Suplentes [2] para local, [3] para visitante
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[1].xpath('./following-sibling::tr/td/text()').extract()
			jugadores_numeros = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(0, len(raw_jugadores),3)]
			jugadores_nombres = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),3)]

			club["alineacion"] = [(jugadores_numeros[i], jugadores_nombres[i]) for i in range(0, len(jugadores_numeros))]

			# Alineaciones: [0] para local, [1] para visitante, Suplentes [2] para local, [3] para visitante
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[3].xpath('./following-sibling::tr/td/text()').extract()
			jugadores_numeros = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(0, len(raw_jugadores),3)]
			jugadores_nombres = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),3)]

			club["suplentes"] = [(jugadores_numeros[i], jugadores_nombres[i]) for i in range(0, len(jugadores_numeros))]
		except:
			pass

		try:
			# [0] para local, [1] para visitante
			club["entrenador"] = response.xpath('//td[contains(text(),"Entrenador")]')[1].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8')

			# [2] para local, [3] para visitante
			club["entrenador_2"] = response.xpath('//td[contains(text(),"Entrenador")]')[3].xpath('./following-sibling::td/text()')[0].extract().strip().encode('utf-8')
		except:
			pass


		acta["club_visitante"] = club 


		# Potser trucar a la url_acta2 dinse de parse_acta1,
		# passant url_acta2 dins de l'ActaItem


		request = scrapy.Request(
				acta['urls'][1],
				callback=self.parse_acta2,
				dont_filter=True)
		request.meta['item'] = acta
		yield request # request call back from each page

	def parse_acta2(self, response):

		acta = response.meta['item']

		club_local = acta['club_local']
		club_visitante = acta['club_visitante']



		# Equipo LOCAL

		'''
			Sustituciones: 
				[0] para local, [1] para visitante
			Goles:
				[2] para local, [3] para visitante
			Tarjetas:
				[4] para local, [5] para visitante
		'''
		try:

			# Sustituciones
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[0].xpath('./following-sibling::tr/td/text()').extract()

			entra = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),4)]
			sale = [raw_jugadores[i].strip().encode('utf-8') for i in range(3, len(raw_jugadores),4)]
			minuto = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(1, len(raw_jugadores),4)]

			club_local["sustituciones"] = [{"entra":entra[i], "sale":sale[i], "minuto":minuto[i]} for i in range(0,len(entra))]

			# Goles
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[2].xpath('./following-sibling::tr/td/text()').extract()
			
			goleador = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),2)]
			tipo_gol = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),2)]
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[2].xpath('./following-sibling::tr/td/span/text()').extract()
			minuto_gol = [int(re.findall('\d+',raw_jugadores[i].strip().encode('utf-8'))[0]) for i in range(0, len(raw_jugadores),1)]

			club_local["goles"] = [{"goleador":goleador[i], "tipo_gol":tipo_gol[i], "minuto":minuto_gol[i]} for i in range(0,len(goleador))]

			# Tarjetas
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[4].xpath('./following-sibling::tr/td/text()').extract()

			jugador = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),2)]
			tarjeta = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),2)]
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[4].xpath('./following-sibling::tr/td/span/text()').extract()
			minuto_tarjeta = [int(re.findall('\d+',raw_jugadores[i].strip().encode('utf-8'))[0]) for i in range(0, len(raw_jugadores),1)]

			club_local["tarjetas"] = [{"jugador":jugador[i], "tarjeta":tarjeta[i], "minuto":minuto_tarjeta[i]} for i in range(0,len(jugador))]
		
		except:
			pass

		acta["club_local"] = club_local


		# Equipo VISITANTE

		'''
			Sustituciones: 
				[0] para local, [1] para visitante
			Goles:
				[2] para local, [3] para visitante
			Tarjetas:
				[4] para local, [5] para visitante
		'''
		try:

			# Sustituciones
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[1].xpath('./following-sibling::tr/td/text()').extract()

			entra = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),4)]
			sale = [raw_jugadores[i].strip().encode('utf-8') for i in range(3, len(raw_jugadores),4)]
			minuto = [int(raw_jugadores[i].strip().encode('utf-8')) for i in range(1, len(raw_jugadores),4)]

			club_visitante["sustituciones"] = [{"entra":entra[i], "sale":sale[i], "minuto":minuto[i]} for i in range(0,len(entra))]

			# Goles
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[3].xpath('./following-sibling::tr/td/text()').extract()
			
			goleador = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),2)]
			tipo_gol = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),2)]
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[3].xpath('./following-sibling::tr/td/span/text()').extract()
			minuto_gol = [int(re.findall('\d+',raw_jugadores[i].strip().encode('utf-8'))[0]) for i in range(0, len(raw_jugadores),1)]

			club_visitante["goles"] = [{"goleador":goleador[i], "tipo_gol":tipo_gol[i], "minuto":minuto_gol[i]} for i in range(0,len(goleador))]

			# Tarjetas
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[5].xpath('./following-sibling::tr/td/text()').extract()

			jugador = [raw_jugadores[i].strip().encode('utf-8') for i in range(0, len(raw_jugadores),2)]
			tarjeta = [raw_jugadores[i].strip().encode('utf-8') for i in range(1, len(raw_jugadores),2)]
			raw_jugadores = response.xpath('//tr[contains(./td/text(),"Jugador")]')[5].xpath('./following-sibling::tr/td/span/text()').extract()
			minuto_tarjeta = [int(re.findall('\d+',raw_jugadores[i].strip().encode('utf-8'))[0]) for i in range(0, len(raw_jugadores),1)]

			club_visitante["tarjetas"] = [{"jugador":jugador[i], "tarjeta":tarjeta[i], "minuto":minuto_tarjeta[i]} for i in range(0,len(jugador))]
					
		except:
			pass

		acta["club_visitante"] = club_visitante


		yield acta













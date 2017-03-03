from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from pandas import Series

class GTrend:

	base_uri = 'https://trends.google.com/trends/explore?'
	delay = 1

	def __init__(self, search_term):
		self.search_term = search_term
		self.raw = []
		self.normalized = []
		self.time_points = []
		self.index = []

		self.range_type = ''
		self.stdt = ''
		self.endt = ''
		self.full_year = ''
		self.sttm = ''
		self.entm = ''

		self.country = ''
		self.category = ''
		self.search_type = ''

	# Retrieve data, parse, clean, and normalize
	def retrieve(self):
		sleep(self.delay)
		req_uri = self.__build_uri()
		
		driver = webdriver.PhantomJS()
		driver.get(req_uri)
		sleep(10)
		
		elem = driver.find_element_by_xpath('html')
		response = elem.get_attribute('outerHTML')
		driver.quit()
		'''
		f = open('out.html')
		response = f.read()
		'''
		self.__parse(response)
		self.__clean()

	# Set the date and possibly time range
	def set_range(self, rtype, stdt_year=None, endt=None, sttm=None, entm=None):
		self.range_type = rtype

		# Custom date format as follows '2017-12-31'
		if rtype.lower() == 'custom':
			self.stdt = stdt_year
			self.endt = endt
		elif rtype.lower() == 'custom_year':
			self.full_year = stdt_year
		# Times should be integers representing hour of the day GMT as '00','01',...'23'
		elif rtype.lower() == 'custom_last_week':
			self.stdt = stdt_year
			self.endt = endt
			self.sttm = sttm
			self.entm = entm

	# Country selector
	def set_country(self, country):
		self.country = country.upper()

	# Category selector
	def set_category(self, category):
		self.category = category

	# Indicate type of search trend
	def set_search_type(self, search_type):
		self.search_type = search_type

	# Get the correlation between two trends
	def get_corr(self, cmp_trend):
		series_a = Series(self.normalized, self.index)
		series_b = Series(cmp_trend.normalized, cmp_trend.index)
		return series_a.corr(series_b)

	# Build the uri using all parameters specified
	def __build_uri(self):
		req_uri = self.base_uri
		if self.category != '':
			req_uri += 'cat=' + self.category + '&'

		range_translation = self.__get_range_translation()
		req_uri += range_translation

		if self.country != '':
			req_uri += 'geo=' + self.country + '&'

		if self.search_type != '':
			req_uri += 'gprop=' + self.search_type + '&'

		req_uri += 'q=' + self.search_term.replace(' ', '%20')
		return req_uri

	# Use default (five years) if it doesn't match anything
	def __get_range_translation(self):
		if self.range_type == '':
			return ''

		translation = 'date='
		if self.range_type.lower() == 'hour':
			translation += 'now%201-H'
		elif self.range_type.lower() == '4hours':
			translation += 'now%204-H'
		elif self.range_type.lower() == 'day':
			translation += 'now%201-d'
		elif self.range_type.lower() == '7days':
			translation += 'now%207-d'
		elif self.range_type.lower() == '30days':
			translation += 'today%201-m'
		elif self.range_type.lower() == '90days':
			translation += 'today%203-m'
		elif self.range_type.lower() == 'year':
			translation += 'today%2012-m'
		elif self.range_type.lower() == 'all':
			translation += 'all'
		elif self.range_type.lower() == 'custom':
			translation += self.stdt + '%20' + self.endt
		elif self.range_type.lower() == 'custom_year':
			translation += self.custom_year + '-01-01%20' + self.custom_year + '-12-31'
		elif self.range_type.lower() == 'custom_last_week':
			translation += self.stdt + 'T' + self.sttm + '%20' + self.endt + 'T' + self.entm

		translation += '&'
		return translation

	# Use BeautifulSoup to parse raw html data
	# TODO: return status if no data is able to be returned
	# TODO: return status if requested search type is not available
	def __parse(self, trend_html):
		trend_parse = BeautifulSoup(trend_html, 'lxml')
		line_chart = trend_parse.find('line-chart-directive')

		# First get the raw data
		svg_elem = line_chart.find('svg')
		g_elem = svg_elem.find_all('g')
		path_elem = g_elem[4].find('path')
		raw_data = path_elem.get('d')
		raw_data = raw_data.replace('M','')
		self.raw = [list(map(float, (pair.split(',')))) for pair in raw_data.split('L')]
		
		# Get the dates and data normalized from 1 to 100
		point_count = 0
		tbody_elem = line_chart.find('tbody')
		for tr_elem in tbody_elem.find_all('tr'):
			td_elems = tr_elem.find_all('td')
			self.time_points.append(td_elems[0].string.replace('\u202a','').replace('\u202c',''))
			self.normalized.append(int(td_elems[1].string))
			self.index.append(point_count)
			point_count += 1

	# The raw data values have inverted y coordinates so they must inverted again
	def __clean(self):
		max_y = 0.0
		for pair in self.raw:
			if pair[1] > max_y:
				max_y = pair[1]

		for pair in self.raw:
			if pair[1] < max_y:
				pair[1] = pair[1] + (max_y - pair[1]) * 2

import requests
from lxml import html
from lxml.html import Element
from typing import List
from datetime import datetime, timedelta
import json


def get_data_extractor(date: str, stock_symbol: str) -> str:
	# date: 2018-05-16
	stock_number = get_stock_number_from_symbol(stock_symbol)
	payload = {
		"_limit": 500,
		'startDate': date,
		'endDate': str(datetime.now().date()),
		'stock-symbol': stock_number
		}
	def get_data_for_page(page_number):
		url = 'http://www.nepalstock.com/main/stockwiseprices/index/{0}/'.format(page_number)
		res = requests.get(url, params=payload)
		return res.content
	return get_data_for_page

def get_parsed_content(content: str) -> List[Element]:
	tree = html.fromstring(content)
	table = tree.cssselect('.table-hover > tr')			# Select the table with required content
	return table[1:-1]									# Remove headers and footers that are not required

def get_all_data_from_web(data_extractor):
	page_content = data_extractor(1)
	pages = get_pages(page_content)
	print("{0} pages".format(pages))
	data = get_parsed_content(page_content)
	for i in range(2, pages+1):
		page_content = data_extractor(i)
		data.extend(get_parsed_content(page_content)[1:])
	return data

def get_pages(content):
	tree = html.fromstring(content)
	pages = tree.cssselect('.pager > a')
	if not pages:
		return 0
	if is_int(pages[-1].text_content()):
		return int(pages[-1].text_content())
	return len(pages) - 2

def get_date_for_behind_N_days(n):
	date_N_days_ago = datetime.now() - timedelta(days=n)
	return date_N_days_ago.date()

def parse_each_element(element):
	# 8 elements
	elem_list = [el.text_content() for el in element]
	return elem_list

def get_total_data(elements):
	final_data = map(parse_each_element, elements)
	return list(final_data)

def output_to_file(filename, data):
	with open(filename, 'w+') as open_file:
		json.dump(data, open_file, indent=4)

def get_complete_stock_data_from_n_days_back(days, stock_symbol):
	date = get_date_for_behind_N_days(days)
	data_extractor = get_data_extractor(date, stock_symbol)
	content = get_all_data_from_web(data_extractor)
	data = get_total_data(content)
	# data = filter_data(data)
	print("{0} entries".format(len(data)))
	filename = '../data/' + stock_symbol + '.json'
	output_to_file(filename, data)

def get_stock_number_from_symbol(symbol):
	with open('data/symbols_list.json', 'r') as open_file:
		content = json.load(open_file)
	return content[symbol]['symbol_number']

def is_int(string_number):
	try:
		int(string_number)
		return True
	except ValueError:
		return False

def filter_data(data):
	header = data[0]
	data = list(filter(lambda x: x != header, data))
	return data.insert(0, header)

if __name__ == '__main__':
	get_complete_stock_data_from_n_days_back(2000, 'NIB')

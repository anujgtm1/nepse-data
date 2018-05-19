import requests
from lxml import html
import json
import re


def retrieve_raw_data():
	url = 'http://www.nepalstock.com/company'
	payload = {'_limit': 500, 'sector-id': '', 'stock-name': '', 'stock-symbol': ''}
	res = requests.post(url, data=payload)

	tree = html.fromstring(res.content)
	table = tree.cssselect('.my-table > tr')[2:-1]
	return table

def get_clean_data(table):
	data = {}
	for element in table:
		elem_data = get_dict_element(element)
		data.update(elem_data)
	return data

# 0: S.No., 1: logo, 2: name, 3:symbol, 4: sector, 5: detail_link
def get_dict_element(element):
	data = {
		element[3].text_content().strip(): {
			'name': element[2].text_content().strip(),
			'sector': element[4].text_content().strip(),
			'symbol_number': get_symbol_from_element(element)
		}
	}
	return data


def get_symbol_from_element(element):
	link = list(element[5].iterlinks())[0][2]
	y = re.search('http://www.nepalstock.com/company/display/(.+)', link)
	return int(y.group(1))

def output_data(filename, data):
	with open(filename, 'w+') as open_file:
		json.dump(data, open_file, indent=4)

if __name__ == '__main__':
	data = get_clean_data(retrieve_raw_data())
	output_data('../data/symbols_list.json', data)
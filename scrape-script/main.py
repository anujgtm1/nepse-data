from single_symbol import get_complete_stock_data_from_n_days_back
import json

with open('../data/symbols_list.json', 'r') as open_file:
	symbols = json.load(open_file)

for symbol in symbols:
	print(symbol)
	get_complete_stock_data_from_n_days_back(2000, symbol)
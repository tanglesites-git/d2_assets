from concurrent.futures import ThreadPoolExecutor
import json
import os
import re
from re import RegexFlag

from alive_progress import alive_bar

from features import get_assets
from kernal import fp
from kernal import flatten_dict


dictionary = {}

def break_json_into_lines():
	dir_list = fp.json_dir.iterdir()

	with open('test.json', 'w', encoding = "utf-8") as f1:
		pass

	for item in dir_list:
		name = item.name.split('.')[0]
		print(name)
		with open(item, "r", encoding="utf-8") as f:
			json_data = json.load(f)

			flat_items = flatten_dict(json_data)
			size = len(flat_items)

			with open('test.json', 'a', encoding="utf-8") as f1:
				with alive_bar(size) as bar:
					for key, value in flat_items.items():
						new_key = f'{name}_{key}'
						if isinstance(value, bool):
							string = f'{{ "{new_key}": {str(value).lower()} }}'
						elif isinstance(value, int):
							string = f'{{ "{new_key}": {value} }}'
						elif isinstance(value, float):
							string = f'{{ "{new_key}": {value} }}'
						elif isinstance(value, str):
							new_value = re.sub(r'\s+', ' ', value).strip()
							string = f'{{ "{new_key}": "{json.dumps(new_value)[1:-1]}" }}'

						f1.write(string+'\n')
						bar()


def parse_dict(line):
	try:
		v = list(json.loads(line).items())[0]
		key, value = v
		parts = key.split('_')
		name = f'{parts[0]}{parts[1]}'
		if isinstance(value, int):
			if value not in dictionary:
				dictionary[value] = [key]
			else:
				dictionary[value].append(key)
		print(name)
	except json.JSONDecodeError as e:
		print(f"Skipping invalid JSON line: {line.strip()} Error: {e}")

def create_adj_list():
	with open('test.json', 'r', encoding="utf-8") as f2:
		while True:
			line = f2.readline()

			parse_dict(line)

			if not line:
				break

	with open('adjency_list.json', 'w', encoding="utf-8") as f3:
		f3.write(json.dumps(dictionary, indent = 2, ensure_ascii=False))


if __name__ == '__main__':
	get_assets()
	break_json_into_lines()
	create_adj_list()
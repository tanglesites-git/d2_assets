import json

import kernal.logging
from logging import getLogger
from infrastructure import download, download_write_json, write_manifest, read_manifest, read_flatten_write_back, download_write_bytes, request_hook
from kernal import fp, is_file_older_than_7_days
from requests import Session
from requests.adapters import HTTPAdapter
from kernal import secrets
from urllib3.util.retry import Retry

logger = getLogger(__name__)

image_paths = {}
image_path_cache = []
image_value_paths = set()
session = Session()
retries = Retry(
	total = 3,
	backoff_factor = 0.1,
	status_forcelist = [502, 503, 504],
	allowed_methods = {'GET', 'HEAD', 'OPTIONS', 'TRACE'},
	)
session.mount('https://', HTTPAdapter(max_retries = retries))
session.headers.update({'x-api-key': secrets.apikey})


def get_manifest():
	logger.info("Getting manifest")
	return download('https://www.bungie.net/Platform/Destiny2/Manifest', session)


def extract_image_paths(filepath, i, s):
	name_with_ext = str(filepath).split('\\')[-1]
	name = name_with_ext.split('.')[0]

	with open(filepath, 'r', encoding = 'utf-8') as f1:
		json_obj = json.loads(f1.read())
		logger.info(f'Processing Table: {name} - {100 - ((1 - i / s) * 100)}')
		for k, v in json_obj.items():
			ext = str(v).split('.')[-1]
			if ext in {'jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'webp'}:
				new_key = name + '_' + k
				image_paths[new_key] = v
	with open("image_paths.json", 'w', encoding = 'utf-8') as f2:
		f2.write(json.dumps(image_paths, indent = 2, ensure_ascii = False))


def split_into_chunks(lst, n):
	for i in range(0, len(lst), n):
		yield lst[i:i + n]

def get_assets():
	session.hooks['response'] = request_hook
	manifest = get_manifest()
	if is_file_older_than_7_days(fp.manifest_fn):
		manifest = get_manifest()
		write_manifest(manifest)
	manifest = read_manifest()

	json_world_component_content_paths_tuples = manifest['Response']['jsonWorldComponentContentPaths']['en'].items()
	json_size = len(json_world_component_content_paths_tuples)
	json_world_component_content_paths_lists = [
		[fp.json_dir / f'{i}.json' for i, j in json_world_component_content_paths_tuples],
		[f'https://www.bungie.net{j}' for i, j in json_world_component_content_paths_tuples]]
	file_name_parts = json_world_component_content_paths_lists[0]
	url_parts = json_world_component_content_paths_lists[1]
	target_name_parts = [fp.flat_dir / f'{i.name}' for i in file_name_parts]

	json_world_component_content_paths_zipped = zip(file_name_parts, url_parts)
	flatten_destination_and_target_paths_zipped = zip(file_name_parts, target_name_parts)

	# if is_file_older_than_7_days(fp.root / 'manifest.json'):
	for index, item in enumerate(json_world_component_content_paths_zipped):
		download_write_json(item[0], item[1], session, index, json_size)

	for index, item in enumerate(flatten_destination_and_target_paths_zipped):
		read_flatten_write_back(item[0], item[1], index, json_size)

	for index, item in enumerate(target_name_parts):
		extract_image_paths(item, index, len(target_name_parts))

	with open('image_paths.json', 'r', encoding = 'utf-8') as f:
		image_paths = json.loads(f.read())
		for key, value in image_paths.items():
			directory_parts = key.split('_')
			directory = f'{directory_parts[0]}/{directory_parts[-1]}'
			filename_parts = value.split('/')[-1]
			if filename_parts not in image_value_paths:
				image_value_paths.add(filename_parts)
				image_path_cache.append((fp.images_dir / f'{directory}/{filename_parts}',
				                         f'https://www.bungie.net{value}'))
				(fp.images_dir / f'{directory}').mkdir(parents = True, exist_ok = True)

	size = len(image_path_cache)
	for index, item in enumerate(image_path_cache):
		download_write_bytes(item[0], item[1], session, index, size)

	session.close()
	print("DONE.")
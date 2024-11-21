import json
import os
from pathlib import Path

import requests

import kernal.logging
from typing import List, Tuple
from concurrent.futures import ThreadPoolExecutor

from urllib3.util.retry import Retry
from logging import getLogger
from requests import HTTPError, RequestException

logger = getLogger(__name__)

retries = Retry(
	total = 3,
	backoff_factor = 0.1,
	status_forcelist = [502, 503, 504],
	allowed_methods = {'GET', 'HEAD', 'OPTIONS', 'TRACE'},
	)


def request_hook(response, *args, **kwargs):
	logger.info(f"Response Hook: {response.status_code}")


def download(url: str, session):
	try:
		response = session.get(url, stream = True, allow_redirects = True)
		response.raise_for_status()
		logger.debug(json.dumps(dict(response.headers), indent = 2))
		return response.json()
	except Exception as e:
		logger.error(f"Error downloading {url}: {e}")
		raise
	finally:
		response.close()
		logger.info(f"Close Connection {url}")# Ensure the response is closed



def download1(url: str, session):
	try:
		response = session.get(url, stream = True, allow_redirects = True)
		response.raise_for_status()
		logger.debug(json.dumps(dict(response.headers), indent = 2))
		return response.content
	except Exception as e:
		logger.error(f"Error downloading {url}: {e}")
		raise
	finally:
		response.close()
		logger.info(f"Close Connection {url}")# Ensure the response is closed


def download_write_json(filename, url, session, index, size):
	try:
		if not filename.exists():
			response = session.get(url, stream = True, allow_redirects = True)
			response.raise_for_status()
			if response.status_code == 200:
				with open(filename, 'w', encoding = "utf-8") as f:
					f.write(json.dumps(response.json(), indent = 2))
					logger.info(f"Downloaded {filename} - {100 - ((1 - index / size) * 100)}")
		else:
			print(f"Already exits: {filename} - {100 - ((1 - index / size) * 100)}")
	except HTTPError as e:
		if e.response.status_code == 404:
			print(f"Page not found: {filename} (404)")
		else:
			print(f"HTTP error occurred for {filename}: {e}")
	except RequestException as e:
		print(f"Error occurred while making the request to {filename}: {e}")


def download_write_bytes(filename: str, url: str, session: requests.Session, index: int, size: int):
	try:
		if not Path(filename).exists():
			response = session.get(url, stream = True, allow_redirects = True)
			response.raise_for_status()
			if response.status_code == 200:
				with open(filename, 'wb') as f:
					for chunk in response.iter_content(chunk_size = 8192):
						if chunk:
							f.write(chunk)
							logger.info(f"Downloaded {filename} - {100 - ((1 - index / size) * 100)}")
		else:
			print(f"Already exits: {filename} - {100 - ((1 - index / size) * 100)}")
	except HTTPError as e:
		if e.response.status_code == 404:
			print(f"Page not found: {filename} (404)")
		else:
			print(f"HTTP error occurred for {url}: {e}")
	except RequestException as e:
		print(f"Error occurred while making the request to {url}: {e}")


# def download_many(data_list: List[Tuple[str, str]]):
#
# 	new_data = [
# 		[i for i, j in data_list],
# 		[j for i, j in data_list]
# 		]
# 	with ThreadPoolExecutor(max_workers = os.cpu_count() - 1) as executor:
# 		executor.map(download_write, new_data[0], new_data[1])

import json
import os
import time

import kernal.logging
from logging import getLogger
from kernal import fp
from kernal import flatten_dict

logger = getLogger(__name__)

def write_manifest(manifest_dict: dict):
    logger.info("Writing manifest")
    with open(fp.manifest_fn, mode='w', encoding='utf-8') as f:
        f.write(json.dumps(manifest_dict, indent=2, ensure_ascii=False))

def read_manifest():
    logger.info(f"Reading manifest: {fp.manifest_fn}")
    with open(fp.manifest_fn, mode='r', encoding='utf-8') as f:
        return json.loads(f.read())


def read_flatten_write_back(dest, target, index, size):
    try:
        with open(dest, mode='r', encoding='utf-8') as f:
            try:
                json_dict = json.loads(f.read())
            except json.JSONDecodeError as e:
                logger.error(f"Failed to decode JSON from file {dest}: {e}")
                return


        try:
            flat_dict = flatten_dict(json_dict)
            logger.info(f"Flattened dictionary from file: {dest} - {100 - ((1 - index / size) * 100)}")
            with open(target, mode='w', encoding='utf-8') as f1:
                f1.write(json.dumps(flat_dict, indent=2, ensure_ascii=False))
                logger.info(f"Flattened dictionary written to file: {target}")
        except Exception as e:
            logger.error(f"Error flattening dictionary from {dest}: {e}")
            return
    except IOError as e:
        logger.error(f"Failed to read file {dest}: {e}")
    except Exception as e:
        logger.error(f"Unexpected error occurred: {e}")
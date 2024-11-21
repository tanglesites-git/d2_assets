import os
import time


def is_file_older_than_7_days(file_path):
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"File {file_path} does not exist.")
        return True

    # Get the current time
    current_time = time.time()

    # Get the file's last modification time
    file_mod_time = os.path.getmtime(file_path)

    # Calculate the age of the file in days
    file_age_in_days = (current_time - file_mod_time) / (24 * 3600)

    return file_age_in_days > 7


def flatten_dict(d, parent_key='', delimiter='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{delimiter}{k}" if parent_key else k
        if isinstance(v, dict):
            # Recursively flatten dictionaries
            items.extend(flatten_dict(v, new_key, delimiter=delimiter).items())
        elif isinstance(v, list):
            # Handle lists by appending the index to the key
            for i, elem in enumerate(v):
                indexed_key = f"{new_key}{delimiter}{i}"
                if isinstance(elem, dict):
                    # Recursively flatten dictionaries within lists
                    items.extend(flatten_dict(elem, indexed_key, delimiter=delimiter).items())
                else:
                    # Directly add non-dict elements (strings, numbers, etc.)
                    items.append((indexed_key, elem))
        else:
            # Add non-list, non-dict elements
            items.append((new_key, v))
    return dict(items)


def is_image_path(value):
    if not isinstance(value, str):
        return False

    return str(value).split('.')[-1] in {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp'}
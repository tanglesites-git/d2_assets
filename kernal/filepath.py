from pathlib import Path


class FilePath:
	root = Path().cwd()
	manifest_fn = root / 'manifest.json'
	data_dir = root / 'data'
	json_dir = data_dir / 'json'
	images_dir = data_dir / 'images'
	flat_dir = data_dir / 'flat'

	def __init__(self):
		FilePath.data_dir.mkdir(parents = True, exist_ok = True)
		FilePath.json_dir.mkdir(parents = True, exist_ok = True)
		FilePath.images_dir.mkdir(parents = True, exist_ok = True)
		FilePath.flat_dir.mkdir(parents = True, exist_ok = True)


fp = FilePath()

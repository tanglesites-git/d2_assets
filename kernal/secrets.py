import configparser


class Secrets:

	def __init__(self, key: str):
		self.apikey = key


reader = configparser.ConfigParser()
reader.read('d2_assets.ini', encoding = 'utf-8')

secrets = Secrets(
	reader.get('HTTP', 'apikey')
	)

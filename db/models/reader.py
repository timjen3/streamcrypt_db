from db.models.encryption.encryptor import SymmetricKeyCrypt
from .meta.database import DbRoot
import json


class DbReader(DbRoot):
	def __init__(self, symmetric_key):
		self.__CRYPT__ = SymmetricKeyCrypt(symmetric_key)

	def read_all_pages(self):
		for page_num in [p for p in self.__META_INDEX__ if self.__META_INDEX__[p]]:
			for obj in self.read_page_by_obj(page_num):
				decrypted = self.__CRYPT__.decrypt_string(obj)
				obj = json.loads(decrypted)
				print(obj)

	def get(self, id):
		# TODO: I think there's an issue with the math here. Since I am only reading chunks and not accounting for
		# control characters.
		msg = self.get_obj(id)
		decrypted = self.__CRYPT__.decrypt_string(msg)
		print(id, decrypted)

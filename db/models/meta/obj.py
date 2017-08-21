from .database import DbRoot
import json
import math
NULL_CHAR = chr(0).encode("UTF-8")


class Object(DbRoot):
	def __init__(self, id, object, page_num):
		super().__init__()
		self.id = id
		self.object = object
		self.page_num = page_num
		self._padded_bytes = None
		self._raw_bytes = None
		self._number_of_chunks = None
		self._padding = None

	@property
	def raw_bytes(self):
		return json.dumps(self.object).encode("utf-8")

	@property
	def padded_bytes(self):
		if self._padded_bytes is None:
			self._padded_bytes = self.raw_bytes + self.padding
		return self._padded_bytes

	@property
	def chunked(self):
		for i in range(0, self.number_of_chunks):
			yield self.padded_bytes[i*DbRoot.__CHUNK_SIZE__:(i+1)*(DbRoot.__CHUNK_SIZE__)]

	@property
	def number_of_chunks(self):
		if self._number_of_chunks is None:
			raw_length = len(self.raw_bytes)
			if raw_length < DbRoot.__CHUNK_SIZE__:
				return 1
			self._number_of_chunks = math.ceil(raw_length / DbRoot.__CHUNK_SIZE__)
		return self._number_of_chunks

	@property
	def index_meta(self):
		return self.id, self.number_of_chunks, self.page_num

	@property
	def padding(self):
		if self._padding is None:
			raw_length = len(self.raw_bytes)
			if self.number_of_chunks == 1:
				self._padding = NULL_CHAR * (self.__CHUNK_SIZE__ - raw_length)
			else:
				self._padding = NULL_CHAR * (self.__CHUNK_SIZE__ - (raw_length % self.__CHUNK_SIZE__))
		return self._padding


class EncryptedObject(Object):
	__CRYPT__ = None

	def __init__(self, id, object, page_num):
		super().__init__(id, object, page_num)

	@property
	def raw_bytes(self):
		json_string = json.dumps(self.object)
		return self.__CRYPT__.encrypt_string(json_string).encode("utf-8")


class DecryptedObject(Object):
	__CRYPT__ = None

	def __init__(self, id, object, page_num):
		# TODO: Encrypt id as well.
		object = self.__CRYPT__.decrypt_string(object)
		super().__init__(id, object, page_num)

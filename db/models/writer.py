from db.models.encryption.encryptor import SymmetricKeyCrypt
from .meta.obj import EncryptedObject
from .meta.database import DbRoot
from datetime import datetime


class DbWriter(DbRoot):
	def __init__(self, symmetric_key):
		self.__POINTER_LOC_PAGE__ = 0
		self.__POINTER_LOC_OBJ__ = 0
		EncryptedObject.__CRYPT__ = SymmetricKeyCrypt(symmetric_key)
		self.__META_INDEX__[self.__POINTER_LOC_PAGE__] = list()
		self.__WRITE_QUEUE__ = list()

	def _increment_pointer(self):
		if self.__POINTER_LOC_OBJ__ + 1 < DbRoot.__PAGE_SIZE__:
			self.__POINTER_LOC_OBJ__ += 1
		else:
			self.commit()
			self.__POINTER_LOC_PAGE__ += 1
			self.__POINTER_LOC_OBJ__ = 0
			self.__META_INDEX__[self.__POINTER_LOC_PAGE__] = list()

	@property
	def _pointer(self):
		return self.__POINTER_LOC_PAGE__, self.__POINTER_LOC_OBJ__

	def insert(self, id, obj):
		page, obj_num = self._pointer
		dbobj = EncryptedObject(id, obj, self._pointer[0])
		self.__META_INDEX__[page].append(dbobj.index_meta)
		self.__OBJ_INDEX__[dbobj.index_meta[0]] = dbobj.index_meta
		self.__WRITE_QUEUE__.append(dbobj)
		self._increment_pointer()

	def commit(self):
		if len(self.__WRITE_QUEUE__) > 0:
			print("{}: Committing {} objects from the write queue to disk.".format(datetime.utcnow(), len(self.__WRITE_QUEUE__)))
			self.write_objects(self.__WRITE_QUEUE__)

	# TODO: Would be cool if the server did updates, deletes, and upserts when a page is loaded into memory. The
	# to do list could be appended to the page so it doesn't need to be loaded to do those transactions. Doing this
	# makes the database special purpose though because it means there can only be one reader which is slower but
	# it works well for the purpose of this database.
	def upsert(self, obj):
		pass

	def delete(self, obj):
		pass

	def update(self, obj):
		pass

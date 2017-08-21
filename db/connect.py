"""
	What: A stream-able encrypted object database for Python.
	Why: Because keeping a databases in memory is resource expensive and plaintext databases are unsafe.
	How: Will start with json format, but would like to use pickle format because it's a PITA to serialize/deserialize
		Python data types. Many benchmarks will compare Pickling/De-Pickling strictly to serialization techniques but
		will not take into account the extra effort (not to mention processing power) to convert deserialized
		<insert format here> into native, usable data types when a type outside the limited serialized type formats are
		in use. Pickle does have the vulnerability of containing executable code and so either a checksum should be
		added or a different datatype should be used which can be chunk-serialized and supports more
		data types.
	Warning: This code is written by a non-expert in encryption, and so the security can be hardened.
	Author: Timothy Jannace
"""
from db.models.encryption.encryptor import SymmetricKeyCrypt
from db.models.meta import database
from db.models.reader import DbReader
from db.models.writer import DbWriter


class Db:
	def __init__(self, dir, symmetric_key):
		database.DbRoot.__DB_DIR__ = dir
		database.DbRoot.__ENCRYPTOR__ = SymmetricKeyCrypt(symmetric_key)
		self.Writer = DbWriter(symmetric_key)
		self.Reader = DbReader(symmetric_key)

	def insert(self, id, obj):
		self.Writer.insert(id, obj)

	def commit(self):
		self.Writer.commit()


if __name__ == "__main__":
	this_db = Db("db/core", "akiejflc;zEISLFJGHALW9284-183957")
	this_db.Writer.insert(1, "12393030420929030")

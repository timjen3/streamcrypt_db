from db.connect import Db
from dummyobj import obj
import datetime


db = Db("db\\core\\paged", "akiejflc;zEISLFJGHALW9284-183957302")
print("Starting to insert 10k rows... {}".format(datetime.datetime.utcnow()))
# RAW INSERT (DELETE FILES BEFORE RUN)
# for i in range(0, 10):
# db.insert(i, obj)
# DEDUP
# for i in range(0, 10000):
# 	db.insert(i, obj)
# db.commit()
# db.Reader.read_all_pages()
# db.Reader.get(1)
print("Finished... {}".format(datetime.datetime.utcnow()))

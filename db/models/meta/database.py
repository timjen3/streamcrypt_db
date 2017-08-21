"""Writes objects with no knowledge of encryption. Simply focused on length of characters and page limitations.
Basically an object memory map."""
from io import FileIO
import os
OBJ_CONT = chr(3).encode("UTF-8")
END_OF_OBJ = chr(4).encode("UTF-8")


class DbRoot:
	__CHUNK_SIZE__ = 512
	__PAGE_SIZE__ = 1000
	__DB_DIR__ = ""
	__DB_PREFIX__ = "db."
	__META_INDEX__ = dict()
	__OBJ_INDEX__ = dict()

	def meta_or_false(self, id):
		return self.__OBJ_INDEX__.get(id, False)

	def _page_key(self, page_num):
		return "{}{}".format(self.__DB_PREFIX__, page_num)

	def _page_filename(self, page_key):
		return os.sep.join([self.__DB_DIR__, page_key])

	def get_obj(self, id):
		if id not in self.__OBJ_INDEX__:
			return False
		else:
			objmeta = self.__OBJ_INDEX__.get(id)
			pointer_loc = objmeta[0]
			chunks = objmeta[1]
			page_num = objmeta[2]
			with self.open_page(page_num) as fp:
				fp.seek(pointer_loc)
				obj_raw = fp.read((chunks * DbRoot.__CHUNK_SIZE__))
				return obj_raw.replace(OBJ_CONT, b"").replace(END_OF_OBJ, b"")

	def write_objects(self, list_obj):
		paged_objects = {page_num: list() for page_num in set([obj.page_num for obj in list_obj])}
		while len(list_obj) > 0:
			one_obj = list_obj.pop()
			paged_objects[one_obj.page_num].append(one_obj)
		for page_num in paged_objects:
			with self.open_page(page_num, "ab") as fp:
				for obj in paged_objects[page_num]:
					if obj.number_of_chunks == 1:
						out_line = OBJ_CONT + obj.padded_bytes
					else:
						out_line = b"".join([OBJ_CONT + chunk for chunk in obj.chunked])
					fp.write(out_line + END_OF_OBJ)

	def read_page_by_obj(self, page_num):
		with self.open_page(page_num, "rb") as fp:
			fp.seek(0)
			obj = b""
			while True:
				code = fp.read(1)
				if not code:
					break
				code = ord(code.decode("utf-8"))
				if code == 3:
					raw = fp.read(self.__CHUNK_SIZE__)
					obj += raw
				elif code == 4:
					yield obj
					obj = b""

	def open_page(self, page_num, mode="rb"):
		page_key = self._page_key(page_num)
		page_filename = self._page_filename(page_key)
		return FileIO(page_filename, mode)

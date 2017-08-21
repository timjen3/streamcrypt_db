"""Buffered IO encryption. Encrypts and decrypts strings using a symmetric key where strings are buffered where msg
length is divisible by key length with no remainder to allow stream encryption / decryption.  Encryption method is
self-rolled and so you should consider swapping in a hardened method from cryptography or other library.
Author: Timothy Jannace"""
from db.models.meta.database import DbRoot
import math


class EncryptionBase(DbRoot):
	__SYMMETRIC_KEY__ = None
	__SYMMETRIC_ORD_LIST__ = None
	__KEY_LENGTH__ = None

	def __init__(self, key):
		self.symmetric_key = key

	@property
	def symmetric_key_ord_list(self):
		return self.__SYMMETRIC_ORD_LIST__

	@property
	def key_length(self):
		return self.__KEY_LENGTH__

	@property
	def symmetric_key(self):
		return self.__SYMMETRIC_KEY__

	@symmetric_key.setter
	def symmetric_key(self, val):
		self.__SYMMETRIC_KEY__ = val
		self.__SYMMETRIC_ORD_LIST__ = [ord(c) for c in self.__SYMMETRIC_KEY__]
		self.__KEY_LENGTH__ = len(self.__SYMMETRIC_ORD_LIST__)


class SymmetricKeyCrypt(EncryptionBase):
	"""Encrypts/decrypts fixed-length chunks of text using a symmetric key algorithm."""
	def decrypt_string(self, msg):
		_msg_unbuffered = msg.decode("utf-8").strip(chr(0))
		_plaintext = map(self.__decrypt_chunk, self.__chunk_gen(_msg_unbuffered))
		out = list()
		for one_chunk in _plaintext:
			out.extend(one_chunk)
		return "".join(out)

	def encrypt_string(self, msg):
		_encrypted = map(self.__encrypt_chunk, self.__chunk_gen(msg))
		out = list()
		for one_chunk in _encrypted:
			out.extend(one_chunk)
		return "".join(out)

	def __decrypt_chunk(self, chnk):
		msg_ord = [ord(c) for c in list(chnk)]
		return _unhash_lists(msg_ord, self.symmetric_key_ord_list)

	def __encrypt_chunk(self, chnk):
		msg_ord = [ord(c) for c in list(chnk)]
		return _hash_lists(msg_ord, self.symmetric_key_ord_list)

	def __chunk_gen(self, msg):
		iters = len(msg) / self.key_length
		for i in range(0, math.ceil(iters)):
			_msg_sl = msg[self.key_length*i:self.key_length*(i+1)]
			yield _msg_sl


def _unhash_lists(l1, l2):
	return [chr(l1[i] - l2[i]) for i in range(0, len(l1))]


def _hash_lists(l1, l2):
	return [chr(l1[i] + l2[i]) for i in range(0, len(l1))]

import unittest
from .. import numparser as np

class TestNumParser(unittest.TestCase):

	def testStandardNumbers(self):
		self.text2num("ten thousand two-hundred and fifty-four")
		self.text2num("five million, one-hundred-ten thousand, two-hundred and three")

if __name__ == '__main__':
	unittest.main()
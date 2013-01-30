import unittest
import numparser as np

class TestNumParser(unittest.TestCase):
	def assertPass(self, question, answer):
		self.assertEqual(np.text2num(question), answer)
	def testStandardNumbers(self):
		self.assertPass("ten thousand two-hundred and fifty-four", '10254')
		self.assertPass("five million one-hundred-ten thousand two-hundred and three", "5110203")

if __name__ == '__main__':
	unittest.main()
import unittest

class SimpleTestCase(unittest.TestCase): ...
class TransactionTestCase(SimpleTestCase): ...
class TestCase(TransactionTestCase): ...

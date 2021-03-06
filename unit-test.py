#!/usr/bin/python

import doMaths
import unittest

# subclass unittest.TestCase
class TestMaths(unittest.TestCase):
    
    # runs before every test
    def setUp(self):
        self.x = 5
        self.y = 10

    # Fails due to incorrect expectation        
    def testAdd(self):
        result = doMaths.doMaths(self.x, self.y, '+')
        self.assertEqual(result, 20)
        
    def testMult(self):
        result = doMaths.doMaths(self.x, self.y,'*')
        self.assertEqual(result, 50)

    # Fails due to floor    
    def testQuotient(self):
        result = doMaths.doMaths(self.x, self.y,'/')
        self.assertEqual(result, 0.5)
    
    def testDiff(self):
        result = doMaths.doMaths(self.x, self.y,'-')
        self.assertEqual(result, -5)
    
    # Will fail if TypeError not raised
    def testType(self):
        # Test for automatically generated TypeError
        self.assertRaises(TypeError, doMaths.doMaths, 'three', 4, '-')
    
    # Will fail if AssertionError not raised
    def testOpAssertion(self):
        # Test 'operation' assert inside of doMaths module
        self.assertRaises(AssertionError, doMaths.doMaths, 3, 4, '-')
                
if __name__ == '__main__':
    unittest.main()
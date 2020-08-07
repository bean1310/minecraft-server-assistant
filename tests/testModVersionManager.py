#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import shutil
import os
from os.path import join, dirname

from src.ModVersionManager import ModVersionManager

class TestModVersionManager(unittest.TestCase):

    def setUp(self):
        self.__testOutputDir = join(dirname(__file__), '.test-output')
        os.mkdir(self.__testOutputDir)
        self.__testOutPutFilePath = join(self.__testOutputDir, 'data')

    def tearDown(self):
        shutil.rmtree(self.__testOutputDir)

    def testSetAndGet(self):
        modName = "hoge"
        modVersion = "1.12.0"

        modVersionManager = ModVersionManager(self.__testOutPutFilePath)

        modVersionManager.register(modName, modVersion)

        modNameList = modVersionManager.getModNameList()
        self.assertTrue(modName in modNameList)
        
        self.assertEqual(modVersion, modVersionManager.getModVersion(modName))

if __name__ == "__main__":
    unittest.main()
    
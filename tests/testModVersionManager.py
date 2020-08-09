#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import shutil
import os
from os.path import join, dirname

from src.ModVersionManager \
    import ModVersionManager, ModNotFoundError, BadMethodCallError


class TestModVersionManager(unittest.TestCase):

    def setUp(self):
        self.__testOutputDir = join(dirname(__file__), '.test-output')
        os.mkdir(self.__testOutputDir)
        self.__testOutPutFilePath = join(self.__testOutputDir, 'data')

    def tearDown(self):
        del self.__mvm
        shutil.rmtree(self.__testOutputDir)

    def testSetAndGet(self):
        modName = "hoge"
        modVersion = "1.12.0"

        self.__mvm = ModVersionManager(self.__testOutPutFilePath)

        self.__mvm.register(modName, modVersion)

        self.assertIn(modName, self.__mvm.getModNameList())

        self.assertEqual(modVersion, self.__mvm.getModVersion(modName))

    def testStoreAndLoad(self):
        modName = "foo"
        modVersion = "1.12.1"

        self.__mvm = ModVersionManager.getInstance(self.__testOutPutFilePath)

        self.__mvm.register(modName, modVersion)
        self.__mvm.flush()

        del self.__mvm

        self.__mvm = ModVersionManager.getInstance(self.__testOutPutFilePath)

        self.assertEqual(self.__mvm.getModVersion(modName), modVersion)

    def testModNotFoundError(self):
        modName = "neko"
        modVersion = "2.9.9"

        self.__mvm = ModVersionManager.getInstance(self.__testOutPutFilePath)
        self.__mvm.register(modName, modVersion)

        with self.assertRaises(ModNotFoundError):
            self.__mvm.getModVersion("DontRegisterdModName")

        with self.assertRaises(ModNotFoundError):
            self.__mvm.update('DontRegisterdModName', '10.0')

        with self.assertRaises(ModNotFoundError):
            self.__mvm.delete('DontRegisterdModName')

    def testBadMethodCallError(self):
        modName = "hoge"
        modVersion = "1.0"

        self.__mvm = ModVersionManager.getInstance(self.__testOutPutFilePath)

        self.__mvm.register(modName, modVersion)

        newVersion = "1.1"

        with self.assertRaises(BadMethodCallError):
            self.__mvm.register(modName, newVersion)

    # def testDataBaseAccessError(self):
    #     modName = "innu"
    #     modVersion = "1.0"
    #     testDataFilePath = self.__testOutPutFilePath

    #     self.__mvm = ModVersionManager.getInstance(testDataFilePath)

    #     self.__mvm.register(modName, modVersion)
    #     self.__mvm.flush()

    #     os.remove(testDataFilePath)

    #     with self.assertRaises(DataBaseAccessError):
    #         self.__mvm.flush()


if __name__ == "__main__":
    unittest.main()

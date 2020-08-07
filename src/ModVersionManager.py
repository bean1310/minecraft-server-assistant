#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os.path
import sys


class Singleton(object):

    @classmethod
    def getInstance(cls, input):
        if not hasattr(cls, "_instance"):
            cls._instance = cls(input)
        else:
            cls._instance.input = input
        return cls._instance

class ModVersionManagerError(Exception):
    """This Error is Base Error of ModVersionManager
    """

    def __init__(self, message):
        self.message = message

class DataBaseAccessError(ModVersionManagerError):
    """Raised when failed to access database file
    """
    
    pass

class ModNotFoundError(ModVersionManagerError):
    """Raised when mod don't find in database
    """
    pass

class BadMethodCallError(ModVersionManagerError):
    """Raised when wrong call method
    """
    pass

class ModVersionManager(Singleton):

    __modsList = {}
    __dataFilePath = ""

    def __init__(self, dataFilePath):
        """constructor

        Args:
            dataFilePath (string): Data file path of the mod version manager

        Raises:
            DataBaseAccessError: Raised when failed to open database file
        """
        self.__dataFilePath = dataFilePath
        try:
            if os.path.isfile(self.__dataFilePath) == False:
                with open(file=self.__dataFilePath, mode='w') as dataFile:
                    dataFile.write('')
            with open(file=self.__dataFilePath, mode='r') as dataFile:
                self.__modsList = json.load(dataFile)
        except EnvironmentError:
            raise DataBaseAccessError('Failed to open ' + dataFilePath + '\n')

    def register(self, name, version):
        """Register Mod info

        Args:
            name (string): Mod name
            version (string): Mod version

        Raises:
            BadMethodCallError: Raised when calling this method despite mod is already register.
        """
        if name in self.__modsList:
            raise BadMethodCallError(name + " is already registerd. You should use update method.")
        
        self.__modsList[name] = version

    def update(self, name, version):
        """Update Mod info

        Args:
            name (string): Mod name
            version (string): Mod version

        Raises:
            ModNotFoundError: Raised when mod do not registerd
        """
        if name not in self.__modsList:
            raise ModNotFoundError(name + "is not found in database")

        self.__modsList[name] = version

    def delete(self, name):
        """Delete mod info

        Args:
            name (string): Mod name

        Raises:
            ModNotFoundError: Raised when mod do not registerd

        Returns:
            bool: If successed return True
        """
        try:
            del self.__modsList[name]
        except KeyError:
            raise ModNotFoundError(name + "is not found in database")
        return True

    def flush(self):
        """Persist mod info

        Raises:
            DataBaseAccessError: Raised when failed to open database file
        """
        try:
            with open(file=self.__dataFilePath, mode='w') as dataFile:
                json.dump(self.__modsList, dataFile)
        except IOError:
            raise DataBaseAccessError("Failed to persistent")

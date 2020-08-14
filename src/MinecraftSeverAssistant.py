#!/usr/bin/env python3

import argparse
import os
from os.path import dirname, join

from discord_webhook import DiscordEmbed, DiscordWebhook
from dotenv import load_dotenv

from ModVersionManager import ModVersionManager

ENV_FILE_PATH = join(dirname(__file__), '.env')
DATA_FILE_PATH = join(dirname(__file__), 'data.json')


class MinecraftServerAssistant():

    def __init__(self):

        load_dotenv(ENV_FILE_PATH)

        self.__modVersionManager = \
            ModVersionManager.getInstance(DATA_FILE_PATH)
        self.__discordWebHookUrl = \
            os.environ.get('DISCORD_WEBHOOK_URL')

        parser = argparse.ArgumentParser()

        parser.add_argument(
            'mode',
            choices=['start', 'stop', 'restart',
                     'update-mod', 'add-mod', 'list-mod']
        )

        args = parser.parse_args()

        self.__mode = args.mode

    def main(self):

        if self.__mode == 'start':
            self.__start()
        elif self.__mode == 'stop':
            self.__stop()
        elif self.__mode == 'restart':
            self.__restart()
        elif self.__mode == 'update-mod':
            self.__updateMod()
        elif self.__mode == 'add-mod':
            self.__addMod()
        elif self.__mode == 'list-mod':
            self.__showModList()
        else:
            exit

    def __start(self):
        discordWebHook = DiscordWebhook(url=self.__discordWebHookUrl)
        embed = DiscordEmbed(
            title=':rocket: サーバ起動',
            description='動作しているmodは以下です',
            color=8781710)
        modNameList = self.__modVersionManager.getModNameList()
        for modName in modNameList:
            modVersion = self.__modVersionManager.getModVersion(modName)
            embed.add_embed_field(
                name=modName, value=modVersion, inline=False)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()

    def __restart(self):
        discordWebHook = DiscordWebhook(url=self.__discordWebHookUrl)
        embed = DiscordEmbed(
            title=':repeat: サーバ再起動',
            description='動作しているmodは以下です',
            color=16187269)
        modNameList = self.__modVersionManager.getModNameList()
        for modName in modNameList:
            modVersion = self.__modVersionManager.getModVersion(modName)
            embed.add_embed_field(
                name=modName, value=modVersion, inline=False)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()

    def __stop(self):
        discordWebHook = DiscordWebhook(url=self.__discordWebHookUrl)
        embed = DiscordEmbed(
            title=':octagonal_sign: サーバ停止',
            description='サーバを停止しました',
            color=16748165)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()

    def __addMod(self):
        try:
            print(u"追加するMod名を入力してください。")
            modName = input()

            if modName in self.__modVersionManager.getModNameList():
                print(u"すでに追加されているModです．\n更新には，mod-updateコマンドを利用してください")
                return

            print(modName + u"の現在のバージョンを入力してください。")
            modVersion = input()
            print(u"以下のMod情報を登録しますか？[Y/n]")
            print(u"Mod名: " + modName + u" modバージョン: " + modVersion + '\n')
            yesOrNo = input()
            if yesOrNo == '' or yesOrNo == 'y' or yesOrNo == 'Y':
                self.__modVersionManager.register(modName, modVersion)
                self.__modVersionManager.flush()
            else:
                print(u"登録をせずに終了します")
        except KeyboardInterrupt:
            print("add-modコマンドを終了します．")

    def __updateMod(self):
        try:
            print(u"更新するMod名を入力してください。")
            modName = input()

            if modName not in self.__modVersionManager.getModNameList():
                print(u"登録されていないModです．\n登録には，add-modコマンドを利用してください")
                return

            print(modName + u"の更新後のバージョンを入力してください。")
            modVersion = input()
            print(u"以下のMod情報に更新しますか？[Y/n]")
            print(u"Mod名: " + modName + u" modバージョン: " + modVersion + '\n')
            yesOrNo = input()
            if yesOrNo == '' or yesOrNo == 'y' or yesOrNo == 'Y':
                self.__modVersionManager.update(modName, modVersion)
                self.__modVersionManager.flush()
            else:
                print(u"登録をせずに終了します")
        except KeyboardInterrupt:
            print("update-modコマンドを終了します．")

    def __showModList(self):
        print(u"Mod名" + '\t' + u"バージョン")
        for modName in self.__modVersionManager.getModNameList():
            print(modName +
                  '\t' +
                  self.__modVersionManager.getModVersion(modName))

    def __nonInteractiveMode(self):
        pass

        # if functionName == 'start':
        #     discordWebHook = DiscordWebhook(url=discordWebHookUrl)
        #     embed = DiscordEmbed(
        #         title='サーバ起動', description='サーバを起動しました', color=8781710)
        #     embed.add_embed_field(
        #         name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        #     discordWebHook.add_embed(embed)
        #     discordWebHook.execute()
        # elif functionName == 'stop':
        #     discordWebHook = DiscordWebhook(url=discordWebHookUrl)
        #     embed = DiscordEmbed(
        #         title='サーバ停止', description='サーバを停止しました', color=16748165)
        #     embed.add_embed_field(
        #         name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        #     discordWebHook.add_embed(embed)
        #     discordWebHook.execute()
        # elif functionName == 'restart':
        #     discordWebHook = DiscordWebhook(url=discordWebHookUrl)
        #     embed = DiscordEmbed(
        #         title='サーバ再起動', description='サーバを再起動しました', color=16187269)
        #     embed.add_embed_field(
        #         name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        #     discordWebHook.add_embed(embed)
        #     discordWebHook.execute()
        # elif functionName == 'update':
        #     print("Input next version > ")
        #     nextVersion = input()
        #     saveModInfo(nextVersion)
        #     discordWebHook = DiscordWebhook(url=discordWebHookUrl)
        #     embed = DiscordEmbed(
        #         title='Forge更新', description='サーバのForgeを更新しました', color=8758783)
        #     embed.add_embed_field(name=':rewind: 前のバージョン',
        #                           value=nowForgeVersion)
        #     embed.add_embed_field(
        #         name='今のバージョン :fast_forward:', value=nextVersion)
        #     discordWebHook.add_embed(embed)
        #     discordWebHook.execute()
        # elif functionName == 'mod-update':
        #     print("Input next version > ")
        #     nextVersion = input()
        #     saveModInfo(nextVersion)
        #     discordWebHook = DiscordWebhook(url=discordWebHookUrl)
        #     embed = DiscordEmbed(
        #         title='Forge更新', description='サーバのForgeを更新しました', color=8758783)
        #     embed.add_embed_field(name=':rewind: 前のバージョン',
        #                           value=nowForgeVersion)
        #     embed.add_embed_field(
        #         name='今のバージョン :fast_forward:', value=nextVersion)
        #     discordWebHook.add_embed(embed)
        #     discordWebHook.execute()
        # else:
        #     print('non')

    def __setup(self):

        print(u"こんにちは。")
        print(u"これから初期設定を行います。")
        isEnd = False
        while not isEnd:
            print(u"利用しているMod名を入力してください。")
            modName = input()
            print(modName + u"の現在のバージョンを入力してください。")
            modVersion = input()
            print(u"以下のMod情報を登録しますか？[Y/n]")
            print(u"Mod名: " + modName + u" modバージョン: " + modVersion + '\n')
            yesOrNo = input()
            if yesOrNo == '' or yesOrNo == 'y' or yesOrNo == 'Y':
                self.__modVersionManager.register(modName, modVersion)
            else:
                continue

            print(u"modの登録を続けますか？[Y/n]")
            yesOrNo = input()
            if yesOrNo == '' or yesOrNo == 'y' or yesOrNo == 'Y':
                continue
            else:
                isEnd = True


if __name__ == "__main__":
    MinecraftServerAssistant().main()

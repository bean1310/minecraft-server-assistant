#!/usr/bin/env python3

import sys
import urllib.request
import json
import datetime
from discord_webhook import DiscordWebhook, DiscordEmbed
import os
from os.path import join, dirname
from dotenv import load_dotenv

ENV_FILE_PATH =  join(dirname(__file__), '.env')
DATA_FILE_PATH = join(dirname(__file__), 'data')

def main():
    init()
    discordWebHookUrl = os.environ.get('DISCORD_WEBHOOK_URL')
    functionName = sys.argv[1]

    nowForgeVersion = readNowForgeVersion()
    
    if functionName == 'start':
        discordWebHook = DiscordWebhook(url = discordWebHookUrl)
        embed = DiscordEmbed(title='サーバ起動', description='サーバを起動しました', color=8781710)
        embed.add_embed_field(name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()
    elif functionName == 'stop':
        discordWebHook = DiscordWebhook(url = discordWebHookUrl)
        embed = DiscordEmbed(title='サーバ停止', description='サーバを停止しました', color=16748165)
        embed.add_embed_field(name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()
    elif functionName == 'restart':
        discordWebHook = DiscordWebhook(url = discordWebHookUrl)
        embed = DiscordEmbed(title='サーバ再起動', description='サーバを再起動しました', color=16187269)
        embed.add_embed_field(name=':arrow_forward: 今のバージョン', value=nowForgeVersion)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()
    elif functionName == 'update':
        print("Input next version > ")
        nextVersion = input()
        output(nextVersion)
        discordWebHook = DiscordWebhook(url = discordWebHookUrl)
        embed = DiscordEmbed(title='Forge更新', description='サーバのForgeを更新しました', color=8758783)
        embed.add_embed_field(name=':rewind: 前のバージョン', value=nowForgeVersion)
        embed.add_embed_field(name='今のバージョン :fast_forward:', value=nextVersion)
        discordWebHook.add_embed(embed)
        discordWebHook.execute()
    else:
        print('non')

def readNowForgeVersion():
    with open(DATA_FILE_PATH, 'r') as f:
        version = f.read()
    return version

def output(str):
    with open(DATA_FILE_PATH, 'w') as f:
        f.write(str)

def init():
    load_dotenv(ENV_FILE_PATH)
    if os.path.isfile(DATA_FILE_PATH) == False:
        print('Initial setting\n')
        print('Input now forge version >')
        nowVersion = input()
        output(nowVersion)

if __name__ == "__main__":
    main()

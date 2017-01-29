# coding: UTF-8
# functions for knovabot.py

import discord
import json
import asyncio
import requests
import random

botdata = json.load(open('botinfo.json', 'r'))
headers = {'User-Agent': botinfo['User-Agent']}

def redditfetch(msg):
    print ("Fetching data from Reddit...")
    p = msg.split(" ")
    outtext = []

    try:
        if int(p[3]) > 10:
            numitems = 1
        else:
            numitems = int(p[3])
    except IndexError:
        p.append(1)
        numitems = 1

    if len(p)==4 and len(p[1]) > 0 and len(p[2]) > 0 and p[1] != "-help":

        r = requests.get('https://www.reddit.com/r/'+p[1]+'/'+p[2]+'/.json?t=day&limit='+str(numitems), headers=headers)
        print ("Trying this URL: " + 'https://www.reddit.com/r/'+p[1]+'/'+p[2]+'/.json?t=day&limit='+str(numitems))

        if r.status_code == "404" or "error" in r.text:
            print ("Status code: " + str(r.status_code))
            print (r.text)
            outtext = ["Error: " + str(r.text), "Maybe check the formatting of your request. Try !reddit -help"]
            return outtext

        p = json.loads(r.text)

        count = 1
        for subs in p['data']['children']:
            outtext.append(str(count) + ". " + subs['data']['title'] + " | URL: " + subs['data']['url'])
            count += 1



    else:
        print ("Sending help text for the !reddit command due to formatting error or request for -help")
        outtext = ["Usage: !reddit SUBREDDIT sort number-of-items",
                   "Ex: !reddit gaming new 5 <-- this would return 5 new submissions from the gaming subreddit",
                   "'sort' can be one of the following: new / hot / top / random / controversial / rising"
                   ]

    return outtext

def helpmsg():
    helpmsg = [
        "Here are the current commands you can use that I will respond to:",
        "!help will trigger this help message.",
        "!reddit will return a list of reddit posts, use !reddit -help for more info.",
        "!roll <num> will roll a <num>-sided die",
        "!name and !location are both stupid self-referencing commands for this bot."
    ]
    return helpmsg

def roll(msg):
    p = msg.split(" ")
    try:
        if len(p) <= 1:
            num = 6
        else:
            num = int(p[1])
    except ValueError:
        return -1



    return random.randint(1,num)

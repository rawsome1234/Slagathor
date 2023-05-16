from mimetypes import init
import discord
import math
import random
from discord.ext import commands
from discord.ext.commands import CommandOnCooldown
import pymongo
from pymongo import MongoClient
import certifi
import asyncio

prefix = '--'

mongoConnection = "mongodb+srv://mfbot:J3lvXkeAbHnV7kHQ@mfbot.pjgnt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

cluster = MongoClient(mongoConnection, tlsCAFile=certifi.where())



client = commands.Bot(command_prefix = prefix)

@client.event
async def on_ready():
	print("Bot is ready")

@client.command()
async def ping(ctx):
	await ctx.send(f"pong!!! {round(client.latency * 1000)}ms")

@client.command(aliases = ['8ball'])
async def _8ball(ctx, *, question):
    total = 0
    for letter in question:
        total += ord(letter)
    responses = ["It is certain."
    "It is decidedly so.",
    "Without a doubt.",
    "Yes - definitely.",
    "You may rely on it.",
    "As I see it, yes.",
    "Most likely.",
    "Outlook good.",
    "Yes.",
    "Signs point to yes.",
    "Reply hazy, try again.",
    "Ask again later.",
    "Better not tell you now.",
    "Cannot predict now.",
    "Concentrate and ask again.",
    "Don't count on it.",
    "My reply is no.",
    "My sources say no.",
    "Outlook not so good.",
    "Very doubtful."]
    index = total % len(responses)
    await ctx.send(f"Question: {question}\nAnswer: {responses[index]}")

@client.command()
async def quoteget(ctx):
    collection = db["data"]
    user = collection.find({"_id": "quotes"})
    for items in user:
        quotes = items["quotes"]
    index = random.randint(0, len(quotes))
    quote = quotes[index]
    await ctx.send("```" + str(index+1) + ": " + quote + "```")

@client.command()
async def quote(ctx, quote, author="someone", q="t"):
    collection = db["data"]
    quote = [quote, author]
    await ctx.message.delete()
    message = ""
    if(q[0] == "t"):
        message = "```\"" + quote[0] + "\""
    else:
        message = "```" + quote[0]
    if(author != "n"):
        message += " -" + quote[1]
    message += "```"
    await ctx.send(message)
    user = collection.find({"_id": "quotes"})
    for items in user:
        quotes = items["quotes"]
    quotes.append([message])
    collection.update_one({"_id": "quotes"}, {"$set": {"quotes": quotes}})

def setupDatabase(message):
    global db
    db = cluster["slagathor_" + message.guild.id]

client.run()

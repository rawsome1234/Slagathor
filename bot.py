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
import config

prefix = '--'

mongoConnection = "mongodb+srv://mfbot:J3lvXkeAbHnV7kHQ@mfbot.pjgnt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"

cluster = MongoClient(mongoConnection, tlsCAFile=certifi.where())

intents = discord.Intents.all()

client = commands.Bot(command_prefix = prefix, intents = intents)

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
    db = cluster[str(ctx.guild.id)]
    if db == None:
        await ctx.send("You don't have any quotes yet!")
    else:
        collection = db["data"]
        user = collection.find({"_id": "quotes"})
        quotes = []
        for items in user:
            quotes = items["quotes"]
        if len(quotes) == 0:
            await ctx.send("There are no quotes yet!")
        else:
            index = random.randint(0, len(quotes))
            print(index)
            quote = quotes[index][0]
            quote = quote[3:]
            await ctx.send("```" + str((index+1)) + ": " + quote)

@client.command()
async def quote(ctx, quote, author="someone", q="t"):
    db = cluster[str(ctx.guild.id)]
    collection = db["data"]
    quote = [quote, author]
    await ctx.message.delete()
    message = "```\""
    if(q[0] == "t"):
        message += quote[0] + "\""
    else:
        message = quote[0]
    if(author != "n"):
        message += " -" + quote[1]
    message += "```"
    await ctx.send(message)
    user = collection.find({"_id": "quotes"})
    quotes = []
    for items in user:
        quotes = items["quotes"]
    quotes.append([message])
    if len(quotes) == 1:
        collection.insert_one({"_id": "quotes", "quotes": quotes})
    else:
        collection.update_one({"_id": "quotes"}, {"$set": {"quotes": quotes}})

@client.command()
async def slaghelp(ctx, section="p"):
    if section[0] == "q":
        await ctx.send("```--quote [quote (must be in quotations)] [person name] [include quotations]\nCreates a quote based on input.\nThe quote must be in quotations.\nIf person name is 'n', then there will be no person being quoted.\nInclude quotations is true by default. Add 'f' to change it to false.\
            \n\n--quoteget\nNo parameters. Sends a random quote.```")

client.run(config.bot_id)
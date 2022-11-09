import logging
import os
import time

import discord
from discord.ext import commands

from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline

logging.basicConfig(level=logging.INFO)

logging.info("Loading model...")
model_name = "deepset/roberta-base-squad2"
nlp = pipeline('question-answering', model=model_name, tokenizer=model_name, max_answer_len=100)
logging.info("Model loaded")

activity = discord.Game(name="Making you jobless")
bot = commands.Bot(command_prefix='!', description="Experiment QA bot by Toppe#4670", activity=activity)

channels = ["support-bot", "moderator-only", "clients", "support"]


@bot.event
async def on_message(message):
    st = time.perf_counter()

    if message.author.bot or message.reference:
        return

    ctx = await bot.get_context(message)

    if not message.guild:
        await ctx.send("Sorry, I do not answer to private messages.")
        return

    if str(message.channel) not in channels:
        print("ignoring message on channel: %s" % message.channel)
        return

    if not message.content.startswith("!qa"):
        return

    await message.channel.trigger_typing()
    await bot.process_commands(message)

    logging.info("msg: %s", message.content)
    answer = await find_answer(question=message.content[3:])
    logging.info("answer: %s", answer)

    et = time.perf_counter()
    calc_delay = int((et - st) * 1000)

    await ctx.reply(answer)

    logging.info("Answer took {0} ms (total {1} ms)".format(calc_delay, int((time.perf_counter() - st) * 1000)))


async def find_answer(question):
    with open('input_docs.txt', 'r') as content_file:
        context = content_file.read()
        res = nlp({
            'question': question,
            'context': context
        })
        print(res)
        return res['answer']


@bot.event
async def on_ready():
    logging.info("The bot has started.")


if __name__ == "__main__":
    bot.run(os.environ['BOT_TOKEN'])

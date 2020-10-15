import bot_blender
import bot_seq2seq
from bot_seq2seq import *

from flask import Flask, render_template, request


app = Flask(__name__)

bot = None


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/get")
def get_bot_response():
    question = request.args.get('msg')
    try:
        answer = bot.get_answer(question)
    except:
        answer = "sorry, I don't know"
    if not answer:
        answer = "sorry, I don't know"
    return answer


@app.route("/load_seq2seq_model")
def load_seq2seq_model():
    print("loading seq2seq")
    global bot
    bot = bot_seq2seq
    return "loaded seq2seq"


@app.route("/load_blender_model")
def load_blender_model():
    print("loading blender model")
    global bot
    bot = bot_blender
    return "loaded blender"


if __name__ == "__main__":
    bot_blender.SafeInteractive.main("-mf", "zoo:blender/blender_90M/model", "-t", "blended_skill_talk")
    load_blender_model()
    app.run(host='0.0.0.0', port=8080)

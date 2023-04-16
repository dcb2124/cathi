# -*- coding: utf-8 -*-
"""
Created on Thu Apr  6 00:03:08 2023

@author: dcb21
"""

from flask import Flask, request, jsonify, render_template
import requests
import openai
import os
#from dotenv import load_dotenv
import logging

app = Flask(__name__)


def message(role, content):
    return {'role' : role, 'content' : content}

sys_message_raw = """You are Cathi, a language tutor. You converse with User in a language other than English ("Practice Language").

Because User is not fluent, and Cathi’s goal is to help User attain the proficiency of a native speaker, in each of her responses, Cathi always

1. Looks for flaws in the way User has expressed themself. Whenever Cathi spots an error in grammar, spelling, word choice, or speaks in any way that would not sound natural to a native speaker of the language, Cathi politely offers a correction or improvement. 

2. Continues the conversation after having offered the correction, by making further statements or questions on the present topic of discussion.

Here is an example:

User: Ella, mi hija, son cinco meses. antes, no llorando tan mucho. ahora, mucho llora
Cathi: Es mejor decir: "Ella tiene cinco meses. Antes, mi hija no lloraba tanto. Ahora llora mucho." Entiendo, parece que ella puede estar pasando por una etapa difícil en este momento. ¿Podría haber algo que la esté molestando o causando incomodidad? ¿Ha habido algún cambio reciente en su entorno o rutina? 

Cathi always tries to estimate the level of proficiency of User. If User speaks a broken form of the Practice Language, with many errors, or asks a lot of questions about basic words and phrases, User is probably at a low level of proficiency. If User uses complex grammatical constructions correctly and displays a wide vocabulary, User is probably at a high level of proficiency. Cathi attempts to adjust her speech complexity and vocabulary so that User will be challenged, but not overwhelmed or frustrated.

If the user mixes in English words or phrases, it probably means they don't know the word or phrase in the Practice Language, so Cathi tells them the Practice Language translation of that word or phrase.

Cathi starts by asking what language in English he wants to speak. Cathi only speaks in the practice language after that point and does NOT provide the translation along with the practice language unless specifically asked. The only exception is if User asks Cathi to explain a word or phrase Cathi then gives a succinct definition of the words and their grammatical construction in English.
 
Good example: 
    
"""
##
sys_message = message('system', sys_message_raw)
cathi_intro_message = message('assistant', 'Hello, what language would you like to practice?')

history = [sys_message, cathi_intro_message,]

def update_history(role, content):
    history.append(message(role,content))
    

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/ask_cathi", methods=["POST"])   
def ask_cathi():
    data = request.get_json()
    user_input = data.get("input", "")
    
    user_input = user_input
    update_history('user', user_input)
    
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=history,
        max_tokens=150,
        n=1,
        temperature=0.8,
    )

    reply = response.choices[0].message.content.strip() 
    update_history('user', reply)
    return jsonify({"response": reply})
##

@app.route("/explain_selection", methods=["POST"])
def explain_selection():
    data = request.form
    selection = data.get('selection', "")
    prefix = "Explain what this means in English, including grammar, vocabulary and usage in this context: "
    user_input = prefix + selection
    print(user_input)
    explain_context = history + [message('user', user_input)]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=explain_context,
        max_tokens=150,
        n=1,
        temperature=0.8,
    )
    reply = response.choices[0].message.content.strip()
    return jsonify({"explanation": reply})

# run_server = False
# if run_server:
#     if __name__ == "__main__":
#         load_dotenv()
#         openai.api_key = os.getenv("OPENAI_API_KEY")
#         app.run(debug=False)


#test    
#what it should do is you can highight text, and Cathi will explain it in a different window
#add a clear conversation button.
#vocabulary should have a slot for definitions
#needs an export button..

#Tips for the user - Avoid using English if you don't want Cathi to speak English.
#In the explanation window, you can ask further questions.
# you might want to add buttons to control the behavior at the beginning.
# could have options to "Explain this phrase" "define words" "Explain grammar", in context.
#or it could be "I don't understand this phrase" 
#scroll windows insteadof increasing in size.
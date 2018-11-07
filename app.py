import os
import sys
import json
from datetime import datetime
import random
import jieba

import requests
from flask import Flask, request, render_template

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    log('test')
    # when the endpoint is registered as a webhook, it must echo back
    # the 'hub.challenge' value it receives in the query arguments
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == "your verify_token":
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return "Hello world", 200


@app.route('/', methods=['POST'])
def webhook():

    # endpoint for processing incoming messaging events

    data = request.get_json()
    log(data)  # you may not want to log every incoming message in production, but it's good for testing

    if data["object"] == "page":

        for entry in data["entry"]:
            for messaging_event in entry["messaging"]:
                try:

                    if messaging_event.get("message"):  # someone sent us a message

                        sender_id = messaging_event["sender"]["id"]        # the facebook ID of the person sending you the message
                        recipient_id = messaging_event["recipient"]["id"]  # the recipient's ID, which should be your page's facebook ID
                        message_text = messaging_event["message"]["text"]  # the message's text
                        message_processing(sender_id, message_text)
                        #if (message_text in ['你好','幸會','嗨','哈囉','hi','hello']):
                        #    send_message(sender_id, random.choice(["你好","幸會","嗨","哈囉","hi","hello"]))
                        #elif(message_text in ['餓了','12點了','到中午了','想吃東西']):
                        #    send_message(sender_id, random.choice(["去吃點東西吧,我請客","要不要叫外賣","你豬喔"]))
                        #elif(message_text in "google"):
                        #    send_message(sender_id, "https://www.google.com.tw/")
                        #elif(message_text in "有空的職缺"):
                        #    send_message(sender_id, "目前有空的職缺有...")
                        #elif(message_text in "微程小幫手"):
                        #    send_button_message(sender_id)
                        #elif(message_text in "隱藏功能"):
                        #    #send_message(sender_id, "目前有空的職缺有...")
                        #    send_button_message_2(sender_id)
                        #else:
                        #    send_message(sender_id, "你講的東西我聽不懂欸")

                    if messaging_event.get("delivery"):  # delivery confirmation
                        pass

                    if messaging_event.get("optin"):  # optin confirmation
                        pass

                    if messaging_event.get("postback"):  # user clicked/tapped "postback" button in earlier message
                        pass
                except:
                    # 此例外是避免使用者輸入非文字訊息, 導致機器人中止行動
                    continue

    return "ok", 200

def message_processing(sender_id, message_text):
    seg_list = jieba.cut(message_text, cut_all=False, HMM=True)
    seg_list = list(seg_list)
    try:
        for sl in seg_list:
            if (sl in ['你好','幸會','嗨','哈囉','hi','hello']):
                send_message(sender_id, random.choice(["你好","幸會","嗨","哈囉","hi","hello"]))
                break
            elif(sl in ['餓了','12點了','到中午了','想吃東西']):
                send_message(sender_id, random.choice(["去吃點東西吧,我請客","要不要叫外賣","你豬喔"]))
                break
            elif(sl in "google"):
                send_message(sender_id, "https://www.google.com.tw/")
                break
            elif(sl in "有空的職缺"):
                send_message(sender_id, "目前有空的職缺有...")
                break
            elif(sl in "test2"):
                send_message(sender_id, "it works")
                break
            elif(sl in "微程小幫手"):
                send_button_message(sender_id)
                break
            elif(sl in "隱藏功能"):
                send_button_message_2(sender_id)
                break
            elif(sl in "sender_id"):
                send_message(sender_id, "your id is " + sender_id)
                break
            else:
                pass
        sender_message(sender, "能不能說的更簡單呢")
    except:
        send_message(sender_id, "這個是火星文")

def send_message(recipient_id, message_text):

    log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))

    params = {
        "access_token": "your access_token"
    }
    headers = {
        "Content-Type": "application/json"
    }
    data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "text": message_text
        }
    })
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)

def send_button_message_2(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.google.com",
                        "title":"Let's go party party tonight, oh~~oh"
                    },
                    {
                        "type":"web_url",
                        "url":"https://www.google.com",
                        "title":"I'm a robot"
                    },
                    {
                        "type":"postback",
                        "title":"Oh my god",
                        "payload":"目前有應徵的職缺有..."
                    }
                    ]
                }
            }
        }
    })

    log("sending button to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)


def send_button_message(recipient_id):

    message_data = json.dumps({
        "recipient": {
            "id": recipient_id
        },
        "message": {
            "attachment": {
                "type":"template",
                "payload":{
                    "template_type":"button",
                    "text":"What do you want to do next?",
                    "buttons":[
                    {
                        "type":"web_url",
                        "url":"https://www.google.com",
                        "title":"Google"
                    },
                    {
                        "type":"web_url",
                        "url":"https://www.google.com",
                        "title":"公司的官網"
                    },
                    {
                        "type":"postback",
                        "title":"有空的職缺",
                        #"payload":"Payload for send_button_message()"
                        "payload":"目前有應徵的職缺有..."
                    }
                    ]
                }
            }
        }
    })

    log("sending button to {recipient}: ".format(recipient=recipient_id))

    call_send_api(message_data)

def call_send_api(message_data):

    params = {
        "access_token": "your access_token"
    }
    headers = {
        "Content-Type": "application/json"
    }
    
    r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=message_data)
    if r.status_code != 200:
        log(r.status_code)
        log(r.text)


def log(msg, *args, **kwargs):  # simple wrapper for logging to stdout on heroku
    try:
        if type(msg) is dict:
            msg = json.dumps(msg)
        else:
            pass
            msg = str(msg)
            #msg = str(msg, 'utf-8').format(*args, **kwargs)
        #print (u"{}: {}".format(datetime.now(), msg))
    except UnicodeEncodeError:
        pass  # squash logging errors in case of non-ascii text
    sys.stdout.flush()


if __name__ == '__main__':
    app.run(debug=True)


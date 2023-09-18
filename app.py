
from flask import Flask, jsonify, make_response, request
from utils import create_chain
import requests
import os


app = Flask(__name__)

@app.route("/", methods = ['POST'])
def chat():
    if not request.is_json:
        return make_response(
            jsonify(
                {"success": False,
                 "error": "Unexpected error, request is not in JSON format"}),
            400)
    
    try:
        data = request.json
        message = data["events"][0]["message"]["text"]
        replyToken = data["events"][0]["replyToken"]
        chatgpt_chain = create_chain()
        prediction = chatgpt_chain.predict(human_input=message)

        response = jsonify({
            {
                "messages":
                [
                    { "type": "text", 
                      "text": prediction
                      }
                    ],
                "replyToken": replyToken 
                }
        }
        )

        headers = {
            "Authorization": f"Bearer {os.environ['CHANEL_ACCESS_TOKEN']}",
            "Content-type": "application/json"
        }

        requests.post("https://api.line.me/v2/bot/message/reply", json=response, headers=headers)
        
    except:
        return make_response(
            jsonify({"messages": [{"type": "text", "text": f"Unexpected error: failed to send the message ({request.json})"}], "replyToken": data["events"][0]["replyToken"]}))

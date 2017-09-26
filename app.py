# -*- coding: utf-8 -*-
from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse
from twilio.rest import Client
import requests
import json
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
	resp = VoiceResponse()
	resp.say(u"こんにちは。何かお困りですか。はなしおわったら何かキーを押してください。", language="ja-JP", voice="alice")
	resp.record(timeout=10, max_length=30, finish_on_key="1234567890*#", action="/pause", method="POST", recording_status_callback="/record")
	
	return str(resp)

@app.route("/record", methods=['POST'])
def record():

	wavUrl = request.form['RecordingUrl']
	callSid = request.form['CallSid']
	r = requests.get(wavUrl)
	
	watsonUrl = 'https://stream.watson-j.jp/speech-to-text/api/v1/recognize?continuous=true&model=ja-JP_BroadbandModel&word_confidence=true'
	username = os.environ["STT_USERNAME"]
	password = os.environ["STT_PASSWORD"]
	headers = {'Content-Type': 'audio/wav'}
	audio = r.content
	r2 = requests.post(watsonUrl, data=audio, headers=headers, auth=(username, password))
	
	say = u"ごめんなさい、聞き取れませんでした。"
	if(r.status_code == 200):
		res = json.loads(r2.text)
	
		if(len(res['results']) != 0):
			for result in res['results']:
				for alternative in result['alternatives']:
					transcript = alternative['transcript']
			say = transcript
		
	accountSid = os.environ["ACCOUNT_SID"]
	authToken = os.environ["AUTH_TOKEN"]
	client = Client(accountSid, authToken)
	
	call = client.calls(callSid).update(url="https://twimlserver.herokuapp.com/reply?say="+say, method="GET")
	
	return "export success"
	
@app.route("/reply", methods=['GET'])
def reply():

	resp = VoiceResponse()
	resp.say(request.args.get('say'), language="ja-JP", voice="alice")
	
	return str(resp)
	
@app.route("/pause", methods=['POST'])
def pause():

	resp = VoiceResponse()
	resp.pause(length=10)
	resp.redirect('/record', method='POST')
	return str(resp)
	
if __name__ == "__main__":
    app.run()

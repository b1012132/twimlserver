# -*- coding: utf-8 -*-
from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
import requests
import json
import os

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():
	resp = VoiceResponse()
	resp.say(u"こんにちは。何かお困りですか。はなしおわったら何かキーを押してください。", language="ja-JP", voice="alice")
	resp.record(timeout=10, max_length=30, finish_on_key="1234567890*#", recording_status_callback="/record")
	resp.say(u"ごめんなさい。聞き取れませんでした。", language="ja-JP", voice="alice")
	
	return str(resp)

@app.route("/record", methods=['GET', 'POST'])
def record():
	
	resp = VoiceResponse()
	resp.say(u"レコードメソッド", language="ja-JP", voice="alice")
	return str(resp)

	wavUrl = request.form['RecordingUrl']
	r = requests.get(wavUrl)
	
	watsonUrl = 'https://stream.watson-j.jp/speech-to-text/api/v1/sessions?model=ja-JP_BroadbandModel&word_confidence=true'
	username = os.environ["STT_USERNAME"]
	password = os.environ["STT_PASSWORD"]
	headers = {'Content-Type': 'audio/wav'}
	audio = r.content
	r2 = requests.post(url, data=audio, headers=headers, auth=(username, password))
	
	res = json.loads(r2.text)
	if(len(res['results']) == 0):
		say = u"ごめんなさい、聞き取れませんでした。"
	else:
		for result in res['results']:
			for alternative in result['alternative']:
				transcript = alternative['transcript']
				confidence = alternative['confidence']
		say = transcript.encode('utf-8')
		
	resp = VoiceResponse()
	resp.say(say, language="ja-JP", voice="alice")
	
	return str(resp)
	
if __name__ == "__main__":
    app.run()

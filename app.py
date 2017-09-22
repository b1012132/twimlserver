# -*- coding: utf-8 -*-
from flask import Flask
from twilio.twiml.voice_response import VoiceResponse
import requests

app = Flask(__name__)

@app.route("/", methods=['POST'])
def hello():
	resp = VoiceResponse()
	resp.say(u"こんにちは。何かお困りですか。", language="ja-JP", voice="alice")
	resp.Record(timeout=10, maxLength=30, finishOnKey="1234567890*#", recordingStatusCallback="https://twimlserver.herokuapp.com/record")
	
	return str(resp)

@app.route("/record", methods=['POST'])
def record():
	url = request.form['RecordingUrl']
	r = requests.get(url)
	
	wavFile = open(,'w')#File path here
	wavFile.write(r.content)
	wavFile.close()

if __name__ == "__main__":
    app.run()

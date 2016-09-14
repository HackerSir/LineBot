#!/usr/bin/env python
# -*- coding: utf-8 -*-
import random
import requests
import json
from flask import Flask
from flask import request
from flask import abort
from flask import jsonify

app = Flask(__name__)

raul = [u'剪刀',u'石頭',u'布']
def messages(text):
    raul = [u'剪刀',u'石頭',u'布']
    if text in raul :
        return raul[random.randint(0, len(raul)-1)]
    elif u'/author' in text:
        return u'tamama9527'
    elif u'/date' in text:
	return u'新生茶會 9/21（三）\n時間：18：00開始\n地點：語文大樓\n更多詳細資訊請上：http://goo.gl/hkmvuf'
    return u'…'


@app.route('/callback', methods=['POST'])
def callback():
    if not request.json:
        abort(400)
    results = request.json['result']
    print results
    headers = {'Content-Type': 'application/json; charset=UTF-8',
               'X-Line-ChannelID': '',
               'X-Line-ChannelSecret': '',
               'X-Line-Trusted-User-With-ACL': ''}
    #proxies = {'https': 'http://fixie:hX1VocsmNZQCphJ@velodrome.usefixie.com:80'}
    data = {'to': '',
            'toChannel': 1383378250,
            'eventType': '138311608800106203',
            'content': {'contentType': 1,
                        'toType': 1,
                        'text': ''}}
    for result in results:
        if result['eventType']=='138311609100106403':
            if result['content']['opType']==4:
                data['to'] = [result['content']['params'][0]]
                data['content']['text'] = '你好 我是小黑 黑客社的吉祥物\n你能使用的指令有:/date /author\n如果你很無聊,我可以陪你玩剪刀石頭布'
                r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
                print r.text
        elif result['content']['contentType']==8:
            data['to'] = [result['content']['from']]
            data['content']['text'] = u'有貼圖了不起喔 哼～,stkid:'+result['content']['contentMetadata']['STKID']
	    print result
            r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
            print r.text
        else:
            data['to'] = [result['content']['from']]
	    if result['content']['text'] in raul:
		data['content']['text'] = messages(result['content']['text'])
	        if (result['content']['text']==u'剪刀'and data['content']['text']==u'布') or (result['content']['text']==u'布'and data['content']['text']==u'石頭') or(result['content']['text']==u'石頭'and data['content']['text']==u'剪刀'):
			r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
			data['content']['text']=u'QQ 我輸了'
			r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
	    	elif  (data['content']['text']==u'剪刀'and result['content']['text']==u'布') or (data['content']['text']==u'布'and result['content']['text']==u'石頭') or(data['content']['text']==u'石頭'and result['content']['text']==u'剪刀'):
	    		r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
			data['content']['text']=u'哈哈 我贏了！'
			r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
		else:
			r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
                        data['content']['text']=u'平手 再來一次'
                        r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
	    else:
		data['content']['text']=messages(result['content']['text'])
             	r=requests.post('https://trialbot-api.line.me/v1/events',data=json.dumps(data),headers=headers)
            print data
	    print r.text
    return jsonify('OK')

if __name__ == '__main__':
        app.run()

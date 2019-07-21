from flask import Flask, request, abort
import requests
import json
from Project.Config import *
from uncleengineer import thaistock
import email_to
app = Flask(__name__)


def GET_BTC_PRICE():
    data = requests.get('https://bx.in.th/api/')
    BTC_PRICE = data.text.split('BTC')[1].split('last_price":')[1].split(',"volume_24hours')[0]
    return BTC_PRICE




@app.route('/webhook', methods=['POST','GET'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        Reply_token = payload['events'][0]['replyToken']
        print(Reply_token)
        message = payload['events'][0]['message']['text']
        print(message)
        if 'หุ้น' in message :
            ITD = thaistock('ITD')
            Reply_messasge = 'ราคาหุ้น อิตาเลียนไทย ขณะนี้ : {}'.format(ITD)
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
        
        elif "btc" in message :
            Reply_messasge = 'ราคา BITCOIN ขณะนี้ : {}'.format(GET_BTC_PRICE())
            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)


        return request.json, 200

    elif request.method == 'GET' :
        return 'this is method GET!!!' , 200

    else:
        abort(400)

@app.route('/')
def hello():
    return 'hello world book',200

def ReplyMessage(Reply_token, TextMessage, Line_Acees_Token):
    LINE_API = 'https://api.line.me/v2/bot/message/reply'

    Authorization = 'Bearer {}'.format(Line_Acees_Token) ##ที่ยาวๆ
    print(Authorization)
    headers = {
        'Content-Type': 'application/json; charset=UTF-8',
        'Authorization':Authorization
    }

    data = {
        "replyToken":Reply_token,
        "messages":[{
            "type":"text",
            "text":TextMessage,
            "quickReply":{ 
                "items": [
                {
                        "type": "action", 
                        "imageUrl": "https://www.mindphp.com/images/mail.png",
                        "action": {
                        "type": "message",
                        "label": "1. เริ่มส่งอีเมล",
                        "text": "ส่งอีเมล"
                }
            },

            {
                        "type": "action", 
                        "imageUrl": "https://kapongpang.files.wordpress.com/2013/09/canceled.jpg",
                        "action": {
                        "type": "message",
                        "label": "2. ยกเลิกการส่ง",
                        "text": "ยกเลิกการส่ง"
                }
            }
        ]
    }
    }
    ]
    }
    
    data = json.dumps(data) ## dump dict >> Json Object
    r = requests.post(LINE_API, headers=headers, data=data) 
    return 200






Intents = ['ส่งเมล' , 'ส่งอีเมล' , 'อีเมล' , 'Email', 'email', 'mail']

##### Defualt ของ Gmail
Smtp_server_address = 'smtp.gmail.com'

##### ส่วนของคุณ
your_email = 'puttipong.lims@gmail.com'
password = 'Puttipong1#' ### <<<< อย่าลืมใส่อีเมล พาสเวิดของตัวเองนะครับ
server = email_to.EmailServer(Smtp_server_address , 587 , your_email , password)

@app.route('/Mail_Sender', methods = ['POST','GET'])
def SendMail():
    with open('Project\Session.json','r') as data :
        data = json.load(data)
        print(data['Session'])
        if request.method == 'POST':
            payload = request.json

            if payload['events'][0]['type'] == 'follow':
                Reply_token = payload['events'][0]['replyToken']
                Reply_messasge = 'ยินดีต้อนรับสู่บริการ ส่งอีเมล อัตโนมัติค่ะ กรุณาเลือกเมนู "ส่งอีเมล" เพื่อเริ่มต้นค่ะ'
                ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                data['Session'] =  ''
                data['email'] = ''
                data['message'] = ''
                with open('Project\Session.json','w') as wrtie_data :
                    json.dump(data,wrtie_data)
                return '200'


            else:
                message = payload['events'][0]['message']['text']
                if data['Session'] == '' and [i for i in Intents if i in message]:
                    message = payload['events'][0]['message']['text']
                    Reply_token = payload['events'][0]['replyToken']

                    for i in Intents:
                        if i in message:
                            Reply_messasge = 'กรุณาใส่อีเมลที่ต้องการส่ง'
                            ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                            data['Session'] = 'EMAIL'
                            with open('Project\Session.json','w') as wrtie_data :
                                json.dump(data,wrtie_data)
                            return '200'

                elif data['Session'] ==  'EMAIL':
                    
                    if '@' in message:
                        Reply_token = payload['events'][0]['replyToken']
                        message = payload['events'][0]['message']['text']
                        Reply_messasge = 'กรุณาใส่ข้อความที่ต้องการส่ง'
                        ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                        data['Session'] =  'MESSAGE'
                        data['email'] = message
                        with open('Project\Session.json','w') as wrtie_data :
                            json.dump(data,wrtie_data)
                        return '200'

                    else :
                        Reply_token = payload['events'][0]['replyToken']
                        message = payload['events'][0]['message']['text']
                        Reply_messasge = 'อีเมลไม่ถูกต้อง กรุณาตรวจสอบอีเมลใหม่อีกครั้ง'
                        ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                        data['Session'] =  ''
                        data['email'] = ''
                        with open('Project\Session.json','w') as wrtie_data :
                            json.dump(data,wrtie_data)
                        return '200'

                elif data['Session'] ==  'MESSAGE':
                    Reply_token = payload['events'][0]['replyToken']
                    message = payload['events'][0]['message']['text']
                    Reply_messasge = 'กรุณายืนยันการส่งข้อความ'
                    ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                    data['Session'] =  'CONFIRM'
                    data['message'] = message
                    with open('Project\Session.json','w') as wrtie_data :
                            json.dump(data,wrtie_data)
                    return '200'

                elif data['Session'] ==  'CONFIRM':
                    Reply_token = payload['events'][0]['replyToken']
                    message = payload['events'][0]['message']['text']
                    try :
                        server.quick_email(data['email'], 'ทดลองส่งอีเมลผ่าน Line Chatbot',
                        ['ติดตามได้ที่เพจ Pybott', data['message']],
                        style='h2 {color: black}')
                        
                        Reply_messasge = 'การส่งข้อความสำเร็จ'
                        ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                        data['Session'] =  ''
                        with open('Project\Session.json','w') as wrtie_data :
                            json.dump(data,wrtie_data)
                        return '200'
                    except : 
                        Reply_messasge = 'การส่งข้อความล้มเหลวกรุณา ตรวจสอบแล้วทำการส่งใหม่  1. 2 step mobile vertification must be disable 2. Link : https://www.google.com/settings/security/lesssecureapps 3. Link : https://accounts.google.com/DisplayUnlockCaptcha'
                        ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                        data['Session'] =  ''
                        data['email'] = ''
                        data['message'] = ''
                        with open('Project\Session.json','w') as wrtie_data :
                            json.dump(data,wrtie_data)
                        return '200'

                else :
                    Reply_token = payload['events'][0]['replyToken']
                    message = payload['events'][0]['message']['text']
                    Reply_messasge = 'การส่งอีเมลถูกยุติ กรุณาลองใหม่อีกครั้ง กดเมนู ส่งอีเมล'
                    ReplyMessage(Reply_token,Reply_messasge,Channel_access_token)
                    data['Session'] =  ''
                    data['email'] = ''
                    data['message'] = ''
                    with open('Project\Session.json','w') as wrtie_data :
                        json.dump(data,wrtie_data)
                    return '200'

            return '200'
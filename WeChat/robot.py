#coding=utf8
from werobot import WeRoBot

robot = WeRoBot(
    enable_session=True,
    token='parker',
    APP_ID='wx2fb280445fa5d7d3',
    APP_SECRET='d36864aceac36a5a1907695ab8b1664f',
	ENCODING_AES_KEY='nRP1YWs5bhUP0XjsaWLwwlpdzCYKrMEJhGnHQbn0hXN')

def first(message, session):
    if 'first' in session:
        return '你之前给我发过消息'
    session['first'] = True
    return '你之前没给我发过消息'	
	
# @robot.text 修饰的 Handler 只处理文本消息
@robot.text
def echo(message,session):
    return message.source+":"+message.content+"("+first(message, session)+")"

# @robot.image 修饰的 Handler 只处理图片消息
@robot.image
def img(message):
    return message.img
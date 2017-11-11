from aip import AipSpeech
import jieba
from pyaudio import PyAudio,paInt16
import wave
import winsound
import numpy as np
import urllib
import requests
import json
import os
import sys
from pydub import AudioSegment


""" 你的 APPID AK SK  在下方输入你的百度项目id api key 以及SECRET_KEY"""
APP_ID = ''
API_KEY = ''
SECRET_KEY = ''

aipSpeech = AipSpeech(APP_ID, API_KEY, SECRET_KEY)

framerate=8000
NUM_SAMPLES=2000
channels=1
sampwidth=2
TIME=2

def save_file(filename,data):
    '''save the date to the wavfile'''
    wf=wave.open(filename,'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sampwidth)
    wf.setframerate(framerate)
    wf.writeframes(b"".join(data))
    wf.close()

def my_record():
    pa=PyAudio()
    stream=pa.open(format = paInt16,channels=1,
                   rate=framerate,input=True,
                   frames_per_buffer=NUM_SAMPLES)
    buf=[]
    count=0
    while count<TIME*10:#控制录音时间
        string_audio_data = stream.read(NUM_SAMPLES)
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        large_count = np.sum( audio_data > 900 )
        temp = np.max(audio_data)
        if(large_count>=20):
            buf.append(string_audio_data)
        count+=1
        print('.',end='')
    save_file('in.wav',buf)
    stream.close()

# 定义数据流块
chunk=2014
def play():
    wf=wave.open(r"in.wav",'rb')
    p=PyAudio()
    stream=p.open(format=p.get_format_from_width(wf.getsampwidth()),channels=
    wf.getnchannels(),rate=wf.getframerate(),output=True)
    while True:
        data=wf.readframes(chunk)
        if data=="":break
        stream.write(data)
    stream.close()
    p.terminate()
    return 1

# 读取文件
def get_file_content(filePath):
    with open(filePath, 'rb') as fp:
        return fp.read()

# 识别本地文件
def sb():
    sb=aipSpeech.asr(get_file_content('in.wav'), 'wav', 8000, {
    'lan': 'zh',})
    err_no=sb['err_no']
    if(err_no!=0):
        return ""
    result=sb['result'][0]
    print("我："+result)
    return result


def get_hecheng(para):
    result  = aipSpeech.synthesis(para, 'zh', 1, {'vol': 5,'per':4,})
    
    # 识别正确返回语音二进制 错误则返回dict 参照下面错误码
    if not isinstance(result, dict):
        with open('auido.mp3', 'wb') as f:
            f.write(result)
    else:
        print(result['err_no'])

def getHtml(url):  
    page = urllib.request.urlopen(url)
    html = page.read()
    return html  

def mp3_wav():
    sound = AudioSegment.from_mp3('auido.mp3')
    sound.export("auido.wav", format="wav")
    #os.remove("auido.mp3")

def play():
    mp3_wav()
    file ='auido.wav'
    winsound.PlaySound(
    file,
    winsound.SND_FILENAME|winsound.SND_NOWAIT,
    )
def shibie():
    #引用图灵机器人，输入图灵key 以及
    key=''  
    api="http://www.tuling123.com/openapi/api?userid=331232482&key=" + key+"&loc="+urllib.request.quote("河北省石家庄市河北师范大学") + '&info=' 
    while(1):
        my_record()
        print('Over!')
        s=sb();
        if("退出"in s):
            get_hecheng("主人再见！");
            print('机器人: ' + "再见！");
            play();
            sys.exit();
        if(s!=""):
            request=api+urllib.request.quote(s)
            response = getHtml(request)
            dic_json = json.loads(response)
            print('机器人: ' + dic_json['text'])
            get_hecheng(dic_json['text'])
            if 'list' in dic_json.keys():
                print(dic_json['list'])
            if 'url' in dic_json.keys():
                print(dic_json['url'])
            play();
            
            output = open('luyin.txt', 'a')
            output.write("我:"+s+'\n'+"小鱼："+dic_json['text']+'\n')
            output.close()

if __name__ == '__main__':
    print("欢迎使用语音交互系统：")
    shibie()
    

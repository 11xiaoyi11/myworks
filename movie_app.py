# -*- coding:utf-8 -*-
from flask import Flask, jsonify, request,render_template
import requests
import json
import os
import base64

url = "https://api.coze.cn/open_api/v2/chat"

headers = {
    'Authorization': 'Bearer pat_kPxEpPMWvGjJZKnDlAvBsoZodlQUfsj9pJZW9lwrMnXWFyAFGHk91J5LLZLUSPlK',
    'Content-Type': 'application/json',
    'Accept': '*/*',
    'Host': 'api.coze.cn',
    'Connection': 'keep-alive'
}

def get_coze_response(input_text):
    query=input_text
    data = {
    "bot_id": "7389928868875911183",
    "user": "0",
    "conversation_id": "123",
    "query": query,
    "stream": False,}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    if response.ok:
        data=response.json()
        return data["messages"][3]["content"]
    else:
        return 'ERROR: coze访问错误'

app = Flask(__name__)

imagesData=[]

def init_data(img_div_path,txt_div_path,batch_num):
    for i in range(batch_num):
        img_path=os.path.join(img_div_path,f"image_{i}.jpg")
        txt_path=os.path.join(txt_div_path,f"txt_{i}.txt")
        with open(txt_path,'r',encoding='utf-8') as fp:
            content=fp.read()
        with open(img_path, 'rb') as img_file:
            img_stream = img_file.read()
        img_base64 = base64.b64encode(img_stream)
        img_base64_str = img_base64.decode('utf-8')
        data_url = f"data:image/jpeg;base64,{img_base64_str}"
        imagesData.append({'id':i,'src':data_url,'text':content,'marked':False})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ai_response',methods=['POST'])
def ai_response():
    data = request.json
    user_input = data.get('inputText')
    print(user_input)
    ai_response = get_coze_response(user_input)
    return jsonify({'aiResponse': ai_response})

@app.route('/get-images-data')
def get_images_data():
    images_data = imagesData
    return jsonify(images_data)

if __name__ == '__main__':
    init_data("./作业movie_list v1.0/scrapy/douban_images","./作业movie_list v1.0/scrapy/douban_txts",250)
    app.run(debug=True)
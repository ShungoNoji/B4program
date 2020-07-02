import sys
sys.path.append('c:\\users\\s__bl\\appdata\\local\\programs\\python\\python37\\lib\\site-packages')

import pprint
import os
import cognitive_face as CF

from time import sleep
import csv

from PIL import Image

import re

def getRectangle(faceDictionary):#顔部分の位置座標を抽出　Rectangle:長方形
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	right = left + rect['height']
	bottom = top + rect['width']
	return ((left, top), (right, bottom))


KEY = '8479eca12cc140f3a551b20961583786' #入手したapikeyを入力
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

files = os.listdir('img')
facedata_list=[
["filename","true age","estimated age","abs value diffs"]
]

for file in files:#画像ひとつひとつ
	img_url = "img/"+file

	tmp_str=re.split('[_]',file)
	if tmp_str[2]=="2":
		faces = CF.face.detect(img_url, face_id=True, landmarks=True, attributes='age,gender,emotion')

		# 画像読み込み
		reading_img = Image.open(str(img_url))


		for face in faces:#顔ひとつひとつ
			pos=getRectangle(face)
			img1= reading_img.crop((pos[0][0] , pos[0][1], pos[1][0] , pos[1][1]))#(left, upper, right, lower)

			true_age=tmp_str[0]

			facedata_list.append([
			file,
			true_age,
			face["faceAttributes"]["age"],
			])

			#pprint.pprint(faces)
			pprint.pprint(file+"の人の情報を取得しました")
			sleep(3.2)

print("------------------------------------------------")
print(facedata_list)
with open("utk_dataset.csv", "w", encoding="Shift_jis") as f: # 文字コードをShift_JISに指定
	writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(facedata_list)

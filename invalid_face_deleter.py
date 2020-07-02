import sys
sys.path.append('c:\\users\\s__bl\\appdata\\local\\programs\\python\\python37\\lib\\site-packages')

import pprint
import os

import csv

import re

invalid_faces= os.listdir('invalid')
invalid_faces=[i.rstrip(".jpg .JPG") for i in invalid_faces]#DSC09995-1221_2のような形
invalid_faces=[filename.rsplit('_',1) for filename in invalid_faces]
#DSC09995-1221と2に分割[[DSC09995-1221,2],[DSC09996-1221,2]]のように[ファイル名、順番]と格納されている
#DSC_0074-1229_2などにも対処

csv_url=input("このプログラムと同じ場所に不正な顔画像の入った「invalid」ファイルを作成し、不要な顔データを消したいcsvファイルをD&Dしてください")

#フルパスのfacedata.csvとかのうち、「facedata」だけを格納
basename=os.path.splitext(os.path.basename(csv_url))[0]

#リストを先に定義
csv_list=[]
new_list=[]

with open(str(os.path.basename(csv_url))) as f:#csvのデータをcsv_listに入れる
	reader = csv.reader(f)
	csv_list=[row for row in reader]
	new_list=[csv_list.pop(0)]
	#"filename","order","age","gender","anger","comtempt","disgustとかの文字列を保存

	for row in csv_list:
		exist_flag=0
		for filename in invalid_faces:
			if filename[0]==row[0] and filename[1]==row[1]:#DSC09995-1221、2がそれぞれ一致するか調べる
				exist_flag=1

		if exist_flag==0:
			new_list.append(row)#一致するのがなければnew_listに書き込む

with open(basename+"_invalid_deleted.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(new_list)

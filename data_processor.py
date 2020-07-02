import sys
sys.path.append('c:\\users\\s__bl\\appdata\\local\\programs\\python\\python37\\lib\\site-packages')

import pprint
import os
import cognitive_face as CF

from time import sleep
import csv

from PIL import Image
import PIL.ExifTags as ExifTags

from datetime import datetime as dt

def get_exif(fname):
	# 画像ファイルを開く --- (*1)
	im = Image.open(fname)
	# EXIF情報を辞書型で得る
	exif = {
		ExifTags.TAGS[k]: v
		for k, v in im._getexif().items()
		if k in ExifTags.TAGS
	}
	# GPS情報を得る --- (*2)
	gps_tags = exif["GPSInfo"]
	gps = {
		ExifTags.GPSTAGS.get(t, t): gps_tags[t]
		for t in gps_tags
	}
	# 緯度経度情報を得る --- (*3)
	def conv_deg(v):
		# 分数を度に変換
		d = float(v[0][0]) / float(v[0][1])
		m = float(v[1][0]) / float(v[1][1])
		s = float(v[2][0]) / float(v[2][1])
		return d + (m / 60.0) + (s / 3600.0)
	lat = conv_deg(gps["GPSLatitude"])
	lat_ref = gps["GPSLatitudeRef"]
	if lat_ref != "N": lat = 0 - lat
	lon = conv_deg(gps["GPSLongitude"])
	lon_ref = gps["GPSLongitudeRef"]
	if lon_ref != "E": lon = 0 - lon

	#35mm換算を得る
	thirtyfivemm_equivalent=exif["FocalLengthIn35mmFilm"]

	#撮影時刻を得る
	tdatetime=dt.strptime(exif["DateTimeOriginal"],'%Y:%m:%d %H:%M:%S')

	yobi_list = ["月","火","水","木","金","土","日"]
	yobi=yobi_list[tdatetime.weekday()]

	shooting_date=str(tdatetime.year)+"/"+str(tdatetime.month)+"/"+str(tdatetime.day)
	shooting_hour_and_minute=str(tdatetime.hour)+":"+str(tdatetime.minute)
	shooting_hour=str(tdatetime.hour)

	time_number=0
	if tdatetime.hour==11 or tdatetime.hour==12 or tdatetime.hour==13:
		time_number=1
	if tdatetime.hour==14 or tdatetime.hour==15 or tdatetime.hour==16:
		time_number=2
	if tdatetime.hour==17 or tdatetime.hour==18 or tdatetime.hour==19:
		time_number=3

	return lat, lon, thirtyfivemm_equivalent,yobi,shooting_date,shooting_hour_and_minute,shooting_hour,time_number

def getRectangle(faceDictionary):#顔部分の位置座標を抽出　Rectangle:長方形
	rect = faceDictionary['faceRectangle']
	left = rect['left']
	top = rect['top']
	right = left + rect['height']
	bottom = top + rect['width']
	return ((left, top), (right, bottom))


KEY = '????' #入手したapikeyを入力
BASE_URL = 'https://japaneast.api.cognitive.microsoft.com/face/v1.0'

CF.Key.set(KEY)
CF.BaseUrl.set(BASE_URL)

files = os.listdir('img')
facedata_list=[
["filename","order","age","gender","anger","comtempt","disgust","fear","happiness","neutral","sadness","surprise","Lat","Lon","画像サイズ","35mm換算","曜日","日付","時分","時","時間帯","","","人数","笑顔人数","rate"],
["Average","","=average(C5:C5000)","","=average(E5:E5000)","=average(F5:F5000)","=average(G5:G5000)","=average(H5:H5000)","=average(I5:I5000)","=average(J5:J5000)","=average(K5:K5000)","=average(L5:L5000)","","","","","","","","","","","男性","=COUNTIF(D5:D5000,\"male\")","=COUNTIFS(D5:D5000,\"male\",I5:I5000,\">0.5\")","=Y2/X2"],
["Var","","=VAR.S(C5:C5000)","","=VAR.S(E5:E5000)","=VAR.S(F5:F5000)","=VAR.S(G5:G5000)","=VAR.S(H5:H5000)","=VAR.S(I5:I5000)","=VAR.S(J5:J5000)","=VAR.S(K5:K5000)","=VAR.S(L5:L5000)","","","","","","","","","","","女性","=COUNTIF(D5:D5000,\"female\")","=COUNTIFS(D5:D5000,\"female\",I5:I5000,\">0.5\")","=Y3/X3"],
["STD","","=STDEV.S(C5:C5000)","","=STDEV.S(E5:E5000)","=STDEV.S(F5:F5000)","=STDEV.S(G5:G5000)","=STDEV.S(H5:H5000)","=STDEV.S(I5:I5000)","=STDEV.S(J5:J5000)","=STDEV.S(K5:K5000)","=STDEV.S(L5:L5000)"]
]
for file in files:#画像ひとつひとつ
	img_url = "img/"+file
	faces = CF.face.detect(img_url, face_id=True, landmarks=True, attributes='age,gender,emotion')

	try:
		tuple=get_exif(img_url)
	except KeyError:
		tuple=("","","","","","","","")

	# 画像読み込み
	print(img_url)
	reading_img = Image.open(str(img_url))

	counter=1
	for face in faces:#顔ひとつひとつ
		pos=getRectangle(face)
		img1= reading_img.crop((pos[0][0] , pos[0][1], pos[1][0] , pos[1][1]))#(left, upper, right, lower)
		filename=file.strip(".jpg")+"_"+str(counter)+".jpg"#元ファイル名_通し番号　にする
		img1.save(str("output/"+filename), quality=95)


		facedata_list.append([file.rstrip(".jpg .JPG"),counter,#listにappend
		face["faceAttributes"]["age"],
		face["faceAttributes"]["gender"],
		face["faceAttributes"]["emotion"]["anger"],
		face["faceAttributes"]["emotion"]["contempt"],
		face["faceAttributes"]["emotion"]["disgust"],
		face["faceAttributes"]["emotion"]["fear"],
		face["faceAttributes"]["emotion"]["happiness"],
		face["faceAttributes"]["emotion"]["neutral"],
		face["faceAttributes"]["emotion"]["sadness"],
		face["faceAttributes"]["emotion"]["surprise"],
		tuple[0],#Lat
		tuple[1],#Lat
		pos[1][0]-pos[0][0],#Imagesize
		tuple[2],#35mm換算焦点距離
		tuple[3],#曜日
		tuple[4],#日付
		tuple[5],#時分
		tuple[6],#時
		tuple[7],#時間帯番号
		])
		counter+=1

	if counter==1:
		facedata_list.append([file.rstrip(".jpg .JPG"),"",#listにappend
		"",
		"",
		"",
		"",
		"",
		"",
		"",
		"",
		"",
		"",
		tuple[0],#Lat
		tuple[1],#Lat
		"",#Imagesize
		tuple[2],#35mm換算焦点距離
		tuple[3],#曜日
		tuple[4],#日付
		tuple[5],#時分
		tuple[6],#時
		tuple[7],#時間帯番号
		])
		print("------------------------------------------")
		print(tuple)

	#pprint.pprint(faces)
	pprint.pprint(file+"の人の情報を取得しました")
	sleep(3.2)

print("")
print(facedata_list)
with open("facedata.csv", "w", encoding="Shift_jis") as f: # 文字コードをShift_JISに指定
	writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(facedata_list)

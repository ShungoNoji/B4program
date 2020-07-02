from PIL import Image
import PIL.ExifTags as ExifTags

import os
import csv

from datetime import datetime as dt

def get_gps(fname):
	# 画像ファイルを開く --- (*1)
	im = Image.open(fname)
	# EXIF情報を辞書型で得る
	exif = {
		ExifTags.TAGS[k]: v
		for k, v in im._getexif().items()
		if k in ExifTags.TAGS
	}

	#print(exif)
	print(exif["DateTimeOriginal"])
	tdatetime=dt.strptime(exif["DateTimeOriginal"],'%Y:%m:%d %H:%M:%S' )

	yobi_list = ["月","火","水","木","金","土","日"]
	yobi=yobi_list[tdatetime.weekday()]
	print(yobi)

	shooting_date=str(tdatetime.year)+"/"+str(tdatetime.month)+"/"+str(tdatetime.day)
	shooting_hour_and_minute=str(tdatetime.hour)+":"+str(tdatetime.minute)

	print(shooting_date)
	print(shooting_hour_and_minute)

	time_number=0
	if tdatetime.hour==11 or tdatetime.hour==12 or tdatetime.hour==13:
		time_number=1
	if tdatetime.hour==14 or tdatetime.hour==15 or tdatetime.hour==16:
		time_number=2
	if tdatetime.hour==17 or tdatetime.hour==18 or tdatetime.hour==19:
		time_number=3
	print(tdatetime.hour)
	print(time_number)


	print("=======================================")
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
	return lat, lon

files = os.listdir('img')
gpsdata_list=[]

for file in files:
	img_url = "img/"+file

	try:
		tuple=get_gps(img_url)
	except KeyError:
		tuple=("","")
	gpsdata_list.append([file.strip(".jpg"),tuple[0],tuple[1],])


with open("gpsdata.csv", "w", encoding="Shift_jis") as f: # 文字コードをShift_JISに指定
	writer = csv.writer(f, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(gpsdata_list)

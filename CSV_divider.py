import sys
sys.path.append('c:\\users\\s__bl\\appdata\\local\\programs\\python\\python37\\lib\\site-packages')

import pprint
import os

import csv

import re

# 1.	土日平日すべて
# 2.	土日のみ
# 3.	平日のみ
# 4.	土日の11時から14時
# 5.	土日の14時から17時
# 6.	土日の17時から20時
# 7.	平日の11時から14時
# 8.	平日の14時から17時
# 9.	平日の17時から20時
# 10.	土日平日の11時から14時
# 11.	土日平日の14時から17時
# 12.	土日平日の17時から20時

csv_url=input("分割対象の土日平日全時間が入ったcsvファイルをD&Dしてください")
#フルパスのfacedata.csvとかのうち、「facedata」だけを格納

#リストを先に定義
csv_list=[]#元データ

head=[]#"filename","order","age","gender","anger","comtempt","disgustとかの文字列を保存

weekdays_1=[]#平日の時間帯1
weekdays_2=[]#平日の時間帯2
weekdays_3=[]#平日の時間帯3

weekends_1=[]#土日の時間帯1
weekends_2=[]#土日の時間帯2
weekends_3=[]#土日の時間帯3

#,encoding="utf-8-sig"
with open(str(os.path.basename(csv_url))) as f:#csvのデータをcsv_listに入れる
	reader = csv.reader(f)
	csv_list=[row for row in reader]
	head=[csv_list.pop(0)]

A_all=list(head)
B_weekends=list(head)
C_weekdays=list(head)

D_weekends_1=list(head)
E_weekends_2=list(head)
F_weekends_3=list(head)

G_weekdays_1=list(head)
H_weekdays_2=list(head)
I_weekdays_3=list(head)

J_11_14=list(head)
K_14_17=list(head)
L_17_20=list(head)

for row in csv_list:
	if (row[16]=="月" or row[16]=="火" or row[16]=="水" or row[16]=="木" or row[16]=="金")and row[18]=="2":
		weekdays_2.append(row)

	if (row[16]=="月" or row[16]=="火" or row[16]=="水" or row[16]=="木" or row[16]=="金")and row[18]=="1":
		weekdays_1.append(row)

	if (row[16]=="月" or row[16]=="火" or row[16]=="水" or row[16]=="木" or row[16]=="金" )and row[18]=="3":
		weekdays_3.append(row)

	if (row[16]=="土" or row[16]=="日")and row[18]=="1":
		weekends_1.append(row)

	if (row[16]=="土" or row[16]=="日")and row[18]=="2":
		weekends_2.append(row)

	if (row[16]=="土" or row[16]=="日")and row[18]=="3":
		weekends_3.append(row)

#1
for row in weekends_1,weekends_2,weekends_3,weekdays_1,weekdays_2,weekdays_3:
	A_all+=row

#2
for row in weekends_1,weekends_2,weekends_3:
	B_weekends+=row

#3
for row in weekdays_1,weekdays_2,weekdays_3:
	C_weekdays+=row

#4
for row in weekends_1:
	D_weekends_1+=[row]

#5
for row in weekends_2:
	E_weekends_2+=[row]

#6
for row in weekends_3:
	F_weekends_3+=[row]

#7
for row in weekdays_1:
	G_weekdays_1+=[row]

#8
for row in weekdays_2:
	H_weekdays_2+=[row]

#9
for row in weekdays_3:
	I_weekdays_3+=[row]

#10
for row in weekends_1,weekdays_1:
	J_11_14+=row

#11
for row in weekends_2,weekdays_2:
	K_14_17+=row

#12
for row in weekends_3,weekdays_3:
	L_17_20+=row

print("数チェック用")
print(int(len(A_all)-1))
print(int(len(B_weekends+C_weekdays))-2)
print(int(len(D_weekends_1+E_weekends_2+F_weekends_3+G_weekdays_1+H_weekdays_2+I_weekdays_3)-6))
print(int(len(J_11_14+K_14_17+L_17_20))-3)

print("-----------------")
print("-----------------")

print(int(len(A_all))-1)
print("-----------------")
print(int(len(B_weekends))-1)
print(int(len(C_weekdays))-1)
print("-----------------")
print(int(len(D_weekends_1))-1)
print(int(len(E_weekends_2))-1)
print(int(len(F_weekends_3))-1)
print("-----------------")
print(int(len(G_weekdays_1))-1)
print(int(len(H_weekdays_2))-1)
print(int(len(I_weekdays_3))-1)
print("-----------------")
print(int(len(J_11_14))-1)
print(int(len(K_14_17))-1)
print(int(len(L_17_20))-1)


with open("01_all.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(A_all)

with open("02_weekends.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(B_weekends)

with open("03_weekdays.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(C_weekdays)

with open("04_weekends_1.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(D_weekends_1)

with open("05_weekends_2.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(E_weekends_2)

with open("06_weekends_3.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(F_weekends_3)

with open("07_weekdays_1.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(G_weekdays_1)

with open("08_weekdays_2.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(H_weekdays_2)

with open("09_weekdays_3.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(I_weekdays_3)

with open("10_alldays_1.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(J_11_14)

with open("11_alldays_2.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(K_14_17)

with open("12_alldays_3.csv", "w", encoding="Shift_jis") as g: # 文字コードをShift_JISに指定
	writer = csv.writer(g, lineterminator="\n") # writerオブジェクトの作成 改行記号で行を区切る
	writer.writerows(L_17_20)

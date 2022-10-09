# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 15:57:12 2022

@author: Den
"""
from tkinter import Tk     
from tkinter.filedialog import askopenfilename
from prettytable import PrettyTable
from matplotlib.colors import to_hex
from colorsys import rgb_to_hsv
from PIL import Image


Tk().withdraw() # интерфейс модуля, для указания пути файла
filename = askopenfilename() #  диалогове окно для выбора изображения

img = Image.open(filename) #подгружаем изображение
"""
img = img.convert(  #конвертируем изображение с индексированными цветами
    "P",
    palette=Image.ADAPTIVE,  
    colors=8 #количество цветов в палитре
    )

 # выводим проиндексрованное изображение
"""
img = img.quantize(8,0,1) #конвертируем В изображение с индексированными цветами

                                            #получаем палитру цветов
clrs = img.getcolors()
p_nzero = img.getpalette()[:len(clrs) * 3]


img.show() 
img.close()


listOfColorsRGB = []        #палитра в RGB
listOfColorsHSV = []        #палитра в HSV

p_nzero = list(p_nzero)


for i in range(int(len(p_nzero)/3)):            #находим палитры
        listOfColorsRGB.append((p_nzero[i*3]    
                             ,p_nzero[i*3+1]
                             ,p_nzero[i*3+2]
            ))
        listOfColorsHSV.append(rgb_to_hsv(p_nzero[i*3]/255,
                                          p_nzero[i*3+1]/255,
                                          p_nzero[i*3+2]/255))
        


secTable = {'1':(55,65),        #структура с соответсвиями номера секторов со значением тона
            '2':(45,55),
            '3':(35,45),
            '4':(25,35),
            '5':(15,25),
            '6':(5,15),
            '7':(0,5),
            '8':(330,350),
            '9':(310,330),
            '10':(290,310),
            '11':(270,290),
            '12':(250,270),
            '13':(230,250),
            '14':(210,230),
            '15':(190,210),
            '16':(170,190),
            '17':(150,170),
            '18':(130,150),
            '19':(115,130),
            '20':(105,115),
            '21':(95,105),
            '22':(85,95),
            '23':(75,85),
            '24':(65,75),
            '25':(350,361),
            }

colorSectors = []

for i in range(len(listOfColorsHSV)):       #находим для каждого цвета номер его сектора на цветовом круге
        for l in range(len(secTable)):
            if(listOfColorsHSV[i][0]*360 >= secTable.get(str(l+1))[0] and listOfColorsHSV[i][0]*360 < secTable.get(str(l+1))[1]):
                if(l+1 == 25):
                    colorSectors.append(7)
                else:
                    colorSectors.append(l+1);



t = PrettyTable()  # создаем матрицу PH[4,8] со строками Nкр, H,S,V
t.add_column(" ",['Nкр','H','S','V'])
for n in range(len(listOfColorsRGB)):
    t.add_column(str(to_hex(([i / 255 for i in listOfColorsRGB[n]]))),[colorSectors[n],round(listOfColorsHSV[n][0]*360),round(listOfColorsHSV[n][1]*100),round(listOfColorsHSV[n][2]*100)])
print(t)                                #выводим таблицу

with open("PH.txt", "w") as file: #запись PH в файл
    file.write(str(t))
    
temp = [90,120,150,180,150,120,90,60,30,0,-30,-60,-90,-120,-150,-180,-150,-120,-90,-60,-30,0,30,60] #список температур
    
tempSectors = []
for n in range(len(colorSectors)):      #находим температуру для каждого цвета
    tempSectors.append(temp[colorSectors[n]-1]) 

t = PrettyTable()                       #создаем матрицу DH[5,8] со строками Nкр, H, S, V, Температура 
t.add_column(" ",['Nкр','H','S','V',"Темп"])
for n in range(len(listOfColorsRGB)):
    t.add_column(str(to_hex(([i / 255 for i in listOfColorsRGB[n]]))),[colorSectors[n],round(listOfColorsHSV[n][0]*360),round(listOfColorsHSV[n][1]*100),round(listOfColorsHSV[n][2]*100),tempSectors[n]])
print(t)                            #выводим таблицу

with open("DH.txt", "w") as file:       #запись DH в файл
    file.write(str(t))
    
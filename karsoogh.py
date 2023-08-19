from ast import While
import os
import sys
from os import path
from pickletools import optimize
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import binascii
import tkinter as tk
from tkinter import filedialog
from time import sleep



def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    else:
        app_path = os.path.dirname(os.path.abspath(__file__))
    return  os.path.join(app_path, relative_path)
    # try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    #     base_path = sys._MEIPASS
    #  except Exception:
    #     base_path = os.path.abspath(".")
    # return os.path.join(base_path, relative_path)


saveFormat = ".jpg"
saveQuality = 95
watermarkActive = True
watermarkOpacity = 0.7
watermarkSize = 20

#appdataDir = path.join(path.dirname(__file__),'data')
#fontDir = path.join(appdataDir,'font')
#watermarkDir = path.join(appdataDir, 'watermark')
#fontPath = path.join(fontDir, os.listdir(fontDir)[0])
#watermarkPath = path.join(watermarkDir, os.listdir(watermarkDir)[0])


appdataDir = resource_path("data")
fontDir = resource_path("data\\font")
watermarkDir = resource_path("data\\watermark")
fontPath = path.join(fontDir, os.listdir(fontDir)[0])
watermarkPath = path.join(watermarkDir, os.listdir(watermarkDir)[0])

while True:

    cls = lambda: os.system('cls' if os.name=='nt' else 'clear')
    cls()

    print (f"""Karsoogh Watermark Utility™ (KWU)
Version 1.2.0
Developed by Karsoogh Team
All rights reserved for Karsoogh Mehregan®   



********** Settings ***********

    - Watermark: {watermarkActive}              >> Enter "W" To Change State
    - Watermark Opacity: {watermarkOpacity * 100}%      >> Enter "T" To Change Opacity (from 0 to 100)
    - Watermark Size: 1/{watermarkSize}         >> Enter "S" To Change Size (the bigger the input value, the smaller the size of the applied watermark) (from 1 to 1000)
    - Save Format: {saveFormat}                 >> Enter (1) for JPEG and (2) for PNG
    - Save Quality: {saveQuality}               >> Enter "Q" and then enter your desired quality (from 0 to 100)

************* Enter "O" To Open Files ***********
************* Enter "E" To Exit *****************
""")

    Inp = input()

    if Inp == "1" or Inp == "2":
        if Inp == "1":
            saveFormat = ".jpg"
        if Inp == "2":
            saveFormat = ".png"
        continue

    if Inp == "Q" or Inp == "q":
        print("Enter Quality: ")
        Inp = int(input())
        if Inp >= 0 and Inp <= 100:
            saveQuality = Inp
            print (f"\nQuality successfully set to {saveQuality}")
            sleep(1)
            continue
        else:
            print ("Invalid Value")
            sleep(1)
            continue

    
    if Inp == "T" or Inp == "t":
        print("Enter Opacity: ")
        Inp = int(input())
        if Inp >= 0 and Inp <= 100:
            watermarkOpacity = Inp / 100
            print (f"\nOpacity successfully set to {watermarkOpacity * 100}%")
            sleep(1)
            continue
        else:
            print ("Invalid Value")
            sleep(1)
            continue

    if Inp == "S" or Inp == "s":
        print("Enter Size (Inverse): ")
        Inp = int(input())
        if Inp >= 1 and Inp <= 1000:
            watermarkSize = Inp
            print (f"\nSize successfully set to 1/{watermarkSize}")
            sleep(1)
            continue
        else:
            print ("Invalid Value")
            sleep(1)
            continue

    if Inp == "W" or Inp == "w":
        watermarkActive = not watermarkActive
        continue

    if Inp == "E" or Inp == "e":
        break
    
    if Inp != "o" and Inp != "O":
        print ("Invalid Input")
        sleep(1)
        continue
    
    print("Opening . . .")

    root = tk.Tk()
    root.withdraw()
    root.iconbitmap(path.join(appdataDir,'icon.ico'))

    dirs = filedialog.askopenfilenames(title="Open Picture" , initialdir= '/', filetypes= (("picture files:" , [".png" , ".jpg" , ".jpeg" , ".jpe" , ".gif"]) , ("All files:" , ".") ))
    saveDir = filedialog.askdirectory(title= "Select Where to Save", initialdir = '/')

    for dir in dirs:
        pic = Image.open(dir)
        watermark = Image.open(watermarkPath).convert("RGBA")

        h = pic.size[1]
        watermark.thumbnail((h//watermarkSize,h//watermarkSize))

        watermarked_image = pic.copy()

        savename = ''.join(path.basename(dir).split('.')[:-1])
        savename = str(binascii.crc_hqx(bytes(savename,"utf-8"),0))

        txtLayer = Image.new('RGBA' , pic.size , (255,255,255,0))
        txtDraw = ImageDraw.Draw(txtLayer)
        txtDraw.text((h//(watermarkSize/1.6), h - (h//watermarkSize)), savename, (255, 255, 255, int(255 * watermarkOpacity)), font = ImageFont.truetype(fontPath, h//(watermarkSize * 2)) , anchor="lm")

        if watermarkActive:
            watermarked_image.paste(txtLayer, (0,0) , mask=txtLayer)
            watermarked_image.paste(watermark, (h//(watermarkSize * 2), h - int(h/(watermarkSize * 2) * 3)), mask = Image.eval(watermark,(lambda x: x * watermarkOpacity)))

        print("Saving...   DO NOT CLOSE THE PROGRAM")

        if saveFormat == ".png":
            watermarked_image.save(path.join(saveDir,f"{savename}.png") )
        else:
            watermarked_image = watermarked_image.convert("RGB")
            watermarked_image.save(path.join(saveDir,f"{savename}{saveFormat}"), quality = saveQuality)

        print(f"{savename}{saveFormat} is saved!")
    
    print("""
Operaton Successful
Press Any Key To Continue""")
    Inp = input()
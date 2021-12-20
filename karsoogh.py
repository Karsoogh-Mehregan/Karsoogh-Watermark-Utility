import os
from os import path
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import binascii
import tkinter as tk
from tkinter import filedialog


print ("""Karsoogh Watermark Utility™ (KWU)
Version 1.0.0
Developed by Karsoogh Team
All rights reserved for Karsoogh Mehregan®   






 """)


appdataDir = path.join(path.dirname(__file__),'data')
fontDir = path.join(appdataDir,'font')
watermarkDir = path.join(appdataDir, 'watermark')

fontPath = path.join(fontDir, os.listdir(fontDir)[0])
watermarkPath = path.join(watermarkDir, os.listdir(watermarkDir)[0])

root = tk.Tk()
root.withdraw()
root.iconbitmap(path.join(appdataDir,'icon.ico'))

dirs = filedialog.askopenfilenames(title="Open Picture" , initialdir= '/', filetypes= (("picture files:" , [".png" , ".jpg"]) , ("All files:" , ".") ))
saveDir = filedialog.askdirectory(title= "Select Where to Save", initialdir = './')

for dir in dirs:
    pic = Image.open(dir)
    watermark = Image.open(watermarkPath).convert("RGBA")

    h = pic.size[1]
    watermark.thumbnail((h//20,h//20))

    watermarked_image = pic.copy()

    savename = ''.join(path.basename(dir).split('.')[:-1])
    savename = str(binascii.crc_hqx(bytes(savename,"utf-8"),0))

    txtLayer = Image.new('RGBA' , pic.size , (255,255,255,0))
    txtDraw = ImageDraw.Draw(txtLayer)
    txtDraw.text((h//12.5, h - (h//20)), savename, (255, 255, 255, int(255 * 0.7)), font = ImageFont.truetype(fontPath, h//40) , anchor="lm")

    watermarked_image.paste(txtLayer, (0,0) , mask=txtLayer)

    watermarked_image.paste(watermark, (h//40, h - int( h/40 * 3)), mask = Image.eval(watermark,(lambda x: x * 0.7)))

    print("Saving...   DO NOT CLOSE THE PROGRAM")
    watermarked_image.save(path.join(saveDir,f"{savename}.png"))
    print(f"{savename}.png is saved!")
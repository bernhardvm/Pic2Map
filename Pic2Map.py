import folium
from GPSPhoto import gpsphoto
from folium import IFrame
from PIL import Image
import math
import glob
import os
from exif import Image
import tkinter as tk
from tkinter import simpledialog
import webbrowser


ROOT = tk.Tk()
ROOT.withdraw()

path = simpledialog.askstring(title="Map your pictures", prompt="Put the link where the pictures are stored:")



listdir = os.listdir(path)
i = 0

while(listdir[i].lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')) == False):
    i = i+1

startcoordinates = gpsphoto.getGPSData(path+"/"+listdir[i])
m = folium.Map(location=[startcoordinates["Latitude"],startcoordinates["Longitude"]], zoom_start=12)


for file in os.listdir(path):
    if file.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
        imagefile = file
        coordinates = gpsphoto.getGPSData(path+"/"+imagefile)
        #get direction relative to north clockwise
        with open(path+"/"+imagefile, 'rb') as image_file:
            my_image = Image(path+"/"+imagefile)

        directiondegreesM = my_image.gps_img_direction

        # draw dircetion

        directionline = [[coordinates["Latitude"]-0.00005,coordinates["Longitude"]], [coordinates["Latitude"]-0.00005+math.cos(math.radians(directiondegreesM))*0.0001,coordinates["Longitude"]+math.sin(math.radians(directiondegreesM))*0.0001]]
        m.add_child(folium.CircleMarker([coordinates["Latitude"]-0.00005,coordinates["Longitude"]],fill='true',radius = 6, fill_color='blue', color = 'clear',fill_opacity=1))
        folium.PolyLine(directionline, color="blue", weight=2.5, opacity=1).add_to(m)



        html = '<img src="{}" style="width:400px;height:300px;">'.format(imagefile)
        folium.Marker([coordinates["Latitude"],coordinates["Longitude"]], popup= html, tooltip= imagefile).add_to(m)


m.save(path+"/"+"map.html")
webbrowser.open('file://' + path+"/"+ "map.html", new=2)

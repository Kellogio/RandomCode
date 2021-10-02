# Importing Image from PIL package
from PIL import Image,ImageOps
import requests
from io import BytesIO
import math
import os



URL = "https://pixy.org/src/477/4774988.jpg"
SIZE = (1,1)
X,Y = 100,100
THICKNESS = 1
ANGLE = 45
START = """
G90 G94 G17 G69
G20
G53 G0 Z0
M8
"""
END = "M30"
## i do not need to create a config  because the info are few


# creating a image object


class ImageImporter():
    def __init__(self,url,size) :
        self.__size = size
        self.img = self.__resize(self.__Load(url),size)

    def __resize (self,img,size):
        return img.resize(size)
    def __Load(self,url):
        response = requests.get(url)
        images =  Image.open(BytesIO(response.content))
        if images.mode != "L":
            return ImageOps.grayscale(images)
        return images
    
    @property
    def size(self):
        return self.__size
	
    @size.setter
    def size(self, newsize):
        if isinstance(newsize, tuple) and len(newsize)== 2:
            self.__size = newsize
        else:
            print("Please enter a valid newsize")
    def ReturnArray(self,x,y,Angle,tk):
        listPoint = ""

        for xx in range(0,self.__size[0],x):
            for yy in range(0,self.__size[1],y):
                greyval = self.img.getpixel((xx,yy))*(tk/255)
                z = math.cos(math.radians(Angle))*greyval
                listPoint += PixelPoint(xx,yy,z).GetGCODE()
        return listPoint
class GCodePoint:
    def __init__(self,PixelPoint,Mode):
        self.PixelPoint  = PixelPoint
        self.Mode  = Mode
    def __str__(self):
        return "{0} {1}".format(self.Mode,self.PixelPoint)


class PixelPoint:
    Mov = "G0"
    Lav = "G1"
    def __init__(self,x,y,z):
        self.X = x
        self.Y = y
        self.Z = z

    def _WorkingPoint(self):
        return GCodePoint(ZFeaturePoint(self.X,self.Y,self.Z),self.Lav)
    def _ApproachingPoint(self):
        return GCodePoint(PixelPoint(self.X,self.Y,10),self.Mov)
    def _ContactPointPoint(self):
        return GCodePoint(ZFeaturePoint(self.X,self.Y,0),self.Mov)
    def __Comment(self):
        return " (pixel {0}{1})".format(self.X,self.Y)



    def GetGCODE(self):
        return "\n{3}\n{0}\n{1}\n{2}\n{1}\n{0}\n".format(
        self._ApproachingPoint(),
        self._ContactPointPoint(),
        self._WorkingPoint(),
        self.__Comment()
        )

    def __str__(self):
        return "X{0} Y{1} Z{2}".format(self.X,self.Y,self.Z)

class ZFeaturePoint(PixelPoint):
    def __str__(self):
        return "Z {2}".format(self.X,self.Y,self.Z)
i = ImageImporter(URL,SIZE)
code = i.ReturnArray(X,Y,ANGLE,THICKNESS)
EntireCode = "{0}{1}{2}".format(START,code,END)

with open(os.path.join(os.path.dirname(__file__),"GCODE.gcode"), 'w') as file:
    file.write(EntireCode)

# using getpixel method
#print (img.getpixel(coordinate))
#print(img.getbbox())

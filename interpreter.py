import cv2
import numpy as np

from PIL import Image




class Interpret:
    entryPoint = [0, 0]
    sizeOfLine = 1
    entered = False
    lastPointOnY = []
    motion = "r"
    prevMotion = ""
    instructionMap = {"101": "print",
                      "010": "if",
                      "100": "else",
                      "000": "int",
                      "111": "str",
                      "011": ";"}
    lastInstruction = ""

    def __init__(self, img):
        self.img = cv2.imread(img)

        # Filter
##        self.img[np.where((self.img>=[100,100,100]).all(axis=2))] = [255, 255, 255]
##        self.img[np.where((self.img<=[100, 100, 100]).all(axis=2))] = [0, 0, 0]
        self.showImg(self.img)
        self.maxX = self.img.shape[1]-1
        self.maxY = self.img.shape[0]-1
        for y in range(len(self.img)):
            if not (self.img[y][0] == [255, 255, 255]).all():
                if not self.entered:
                    self.entryPoint = [y, 0]
                    self.entered = True
                else:
                    self.lastPointOnY = y


        self.sizeOfLine = 1

        nextCoords = self.movePointer(*self.entryPoint)
        instructionCode = ""
        y, x = 0, 0

        while True:
            if nextCoords:
                y, x = nextCoords
                nextCoords = self.movePointer(*nextCoords)
            else:
                if instructionCode:
                    instuctionCommand = self.instructionMap.get(instructionCode)
                    if instuctionCommand:
                        self.lastInstruction = instuctionCommand
                    if not instuctionCommand:
                        if len(instructionCode) > 3:
                            instuctionCommand = chr(int(instructionCode, 2))
                            self.execute(instuctionCommand)
                        else:
                            instuctionCommand = ""
##                    if instuctionCommand:
##                        
##                        print(instuctionCommand, end="")
                instructionCode = ""
                if self.motion == "r":
                    y, x = y, x+1

                elif self.motion == "l":
                    y, x = y, x-1

                elif self.motion == "u":
                    y, x = y-1, x

                elif self.motion == "d":
                    y, x = y+1, x
                nextCoords = y, x


            if self.prevMotion != self.motion:
                if (self.img[y][x] == [0, 0, 0]).all():
                    if self.motion == "d":
                        instructionCode = instructionCode+"0"
                    elif self.motion == "u":
                        instructionCode = instructionCode+"1"
                    self.prevMotion = self.motion
                

            if x >= self.maxX or y >= self.maxY :
                print("\nProgram exited with status 0")
                break
##            if nextCoords:
##                y, x = nextCoords
##
##            if x >= self.maxX:
##                break
##            
##            
##            if self.prevMotion != self.motion:
##                print(self.motion)
##                if self.motion == "d":
##                    intructionCode = intructionCode+"0"
##                elif self.motion == "u":
##                    intructionCode = intructionCode+"1"
##                self.prevMotion = self.motion
##                
##
##            if not nextCoords:
##                instuctionCommand = self.instructionMap.get(intructionCode)
##                print("Instruction is", instuctionCommand if instuctionCommand else intructionCode)
##                intructionCode = ""
##                if self.motion == "r":
##                    self.movePointer(y, x+1)
##
##                elif self.motion == "l":
##                    self.movePointer(y, x-1)
##
##                elif self.motion == "u":
##                    self.movePointer(y-1, x)
##
##                elif self.motion == "d":
##                    self.movePointer(y+1, x)
##
##            else:
##                self.movePointer(*nextCoords, intructionCode)


##    def movePointer(self, y, x):
##        nextCoords = self.getNextCoords(y, x)
##        print(nextCoords, self.motion)
##        
##        if nextCoords:
##            self.movePointer(*nextCoords)

    def execute(self, command):
        if self.lastInstruction == "print":
            print(command, end="")

        else:
            return True


    def showImg(self, arr):
        im = Image.fromarray(arr)
        im.show()



    def movePointer(self, y, x, intructionCode=""):
        nextCoords = None
        offset = 1

##        if x >= self.maxX or y >= self.maxY :
##            return

        # Down
        if (self.img[y+offset][x] != [255, 255, 255]).all() and self.motion != "u":
            self.motion = "d"
            nextCoords = [y+offset, x]

        # Up
        elif (self.img[y-offset][x] != [255, 255, 255]).all() and self.motion != "d":
            self.motion = "u"
            nextCoords = [y-offset, x]

        # Right
        elif (self.img[y][x+offset] != [255, 255, 255]).all() and self.motion != "l":
            self.motion = "r"
            nextCoords = [y, x+offset]

        # Left
        elif (self.img[y][x-offset] != [255, 255, 255]).all() and self.motion != "r":
            self.motion = "l"
            nextCoords = [y, x-offset]

        return nextCoords
        

inte = Interpret('images/img.png')

##for y in range(len(img)):
##    for x in range(len(img[y])):
##        if not (img[y][x] == [255, 255, 255]).all():
##            print(img[y][x])

import math

from utils import *


def normalize(channelvalue):                                                                                             # Helper function to keep color values within bounds
    if channelvalue > 255:
        return 255
    return round(channelvalue)

class ImageManager:

    def __init__(self):
        self.img = pygame.image.load("stadium.bmp").convert()
        self.x = 0
        self.y = 0
        self.w = settings.ROWS
        self.h = settings.COLS
        self.angle = 0
        pygame.transform.scale(self.img, (20, 20))



    def setImage(self,imgpath):                                                                                          # Load a Image by taking filename from user
        self.img = pygame.image.load(imgpath).convert()

    def AutoImage(self):                                                                                                 # A default image loader
        self.img = pygame.image.load("stadium.bmp").convert()

    def setX(self,X):
        if(X >= 0 and X < ROWS):
            self.x = X

    def setY(self,Y):
        if (Y >= 0 and Y < ROWS):
            self.y = Y

    def setH(self,H):
        if (H > 0 and H <= COLS):
            self.h = H

    def setW(self,W):
        if (W > 0 and W <= ROWS):
            self.w = W

    def rotate(self,angle):                                                                                              # Rotate the Image
        self.img =  pygame.transform.rotate(self.img, angle)

    def flipVertical(self):                                                                                              # Vertically Flip the Image
        self.img = pygame.transform.flip(self.img,True,False)

    def flipHorizontal(self):                                                                                            # Horizontally Flip the Image
        self.img = pygame.transform.flip(self.img,False,True)

    def applyRedFilter(self):                                                                                            # Apply Red Filter by increasing Red Brightness in all pixels
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                color = self.img.get_at((x, y))
                red, green, blue, alpha = color
                self.img.set_at((x, y), (normalize(1.25*red), normalize(green), normalize(blue), 255))

    def applyGreenFilter(self):                                                                                           # Apply Green Filter by increasing Green Brightness in all pixels
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                color = self.img.get_at((x, y))
                red, green, blue, alpha = color
                self.img.set_at((x, y), (normalize(red), normalize(1.25*green), normalize(blue), 255))

    def applyBlueFilter(self):                                                                                           # Apply Blue Filter by increasing Blue Brightness in all pixels
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                color = self.img.get_at((x, y))
                red, green, blue, alpha = color
                self.img.set_at((x, y), (normalize(red), normalize(green), normalize(1.25*blue), 255))

    def applyGreyScaleFilter(self):                                                                                      # Greyscale the Image by averaging the brightness in all RGB spectrums for all pixels
        for x in range(self.img.get_width()):
            for y in range(self.img.get_height()):
                color = self.img.get_at((x, y))
                red, green, blue, alpha = color
                total = red + green + blue
                average = round(total / 3.0)
                self.img.set_at((x, y), (average, average, average, 255))

    def quicksave(self,window):                                                                                          # quicksave without filename input
        pygame.image.save_extended(window,"quicksave.png")

    def save(self,window,filename):                                                                                      # save with filename input
        pygame.image.save_extended(window,filename)

    def clear(self,grid):                                                                                                # clear the entire grid
        for i in range(ROWS):
            for j in range(COLS):
                grid[j][i] = (255,255,255)

    def render(self,window,grid):                                                                                        # This algorithm takes the average of the pixels which should be present in a block of the grid
                                                                                                                         # Although it is very accurate, it is also very demanding
        NoPixelsInRow = math.floor(self.img.get_width()/self.w)
        NoPixelsInCols = math.floor(self.img.get_height()/self.h)
        TotalPixelInBlock = math.floor(NoPixelsInCols*NoPixelsInCols)

        self.clear(self,grid)                                                                                            # clear the grid before render, otherwise we are left with a mush in the area which should be
                                                                                                                         # clear because of lack of cleanup
        for x in range(self.w):
            for y in range(self.h):
                avgRed = 0
                avgGreen = 0
                avgBlue = 0
                for i in range(NoPixelsInRow):
                    for j in range(NoPixelsInCols):
                        color = self.img.get_at((NoPixelsInRow*x + i,NoPixelsInCols*y + j))                              # get colors of pixels here
                        red, green, blue, alpha = color
                        avgRed   += red                                                                                  # sum red color
                        avgGreen += green                                                                                # sum green color
                        avgBlue  += blue                                                                                 # sum blue color

                avgRed   /= TotalPixelInBlock                                                                            # avg red color
                avgBlue  /= TotalPixelInBlock                                                                            # avg green color
                avgGreen /= TotalPixelInBlock                                                                            # avg blue color
                if (y+self.y < ROWS and x + self.x < COLS):
                    grid[y+ self.y][x + self.x] = (normalize(avgRed),normalize(avgGreen),normalize(avgBlue))             # Assign color to blocks in grid










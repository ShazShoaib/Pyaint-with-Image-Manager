import math
import pygame
import settings
import numpy
import time
from .settings import *
import threading
import pyopencl as cl
import numpy as np
import time


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

    def clear(self,grid):
        # clear the entire grid
        for i in range(ROWS):
            for j in range(COLS):
                grid[j][i] = (255,255,255)

    def renderFast(self,window,grid):
        NoPixelsInRow = (self.img.get_width() / self.w)
        NoPixelsInCols = (self.img.get_height() / self.h)
        Pixels3D = pygame.surfarray.array3d(self.img)
        print(NoPixelsInCols)
        for i in range(COLS):
            for j in range(ROWS):
                grid[i][j] = Pixels3D[math.floor((j+0.5)*NoPixelsInRow)][math.floor((i+0.5)*NoPixelsInCols)]

    def render(self,window,grid):                                                                                        # This algorithm takes the average of the pixels which should be present in a block of the grid
        start = time.time_ns()                                                                  # Although it is very accurate, it is also very demanding
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
        print("RENDER TIME: "+ str((time.time_ns() - start)/1000000000) + "s")



    def renderSurf(self,window,grid):                                                                                   # Same func as render but faster     # This algorithm takes the average of the pixels which should be present in a block of the grid

                                                                                                                  # Although it is very accurate, it is also very demanding
        NoPixelsInRow = (self.img.get_width()/self.w)
        NoPixelsInCols = (self.img.get_height()/self.h)
        TotalPixelInBlock = math.floor(NoPixelsInCols*NoPixelsInCols)
        start = time.time_ns()
        ImgSurface = pygame.Surface.convert(self.img)
        Pixels3D = pygame.surfarray.pixels3d(ImgSurface)
        print("TIME:"+str((time.time_ns()-start)/1000000000)+"s")

        self.clear(self,grid)                                                                                            # clear the grid before render, otherwise we are left with a mush in the area which should be
                                                                                                                         # clear because of lack of cleanup
        for x in range(self.w):
            for y in range(self.h):
                avgRed = 0
                avgGreen = 0
                avgBlue = 0

                for j in range(math.floor(NoPixelsInCols)):
                    for i in range(math.floor(NoPixelsInRow)):
                                      # get colors of pixels here
                        avgRed   += Pixels3D[math.floor(NoPixelsInRow*x + i)][math.floor(NoPixelsInCols*y + j)][0]                                                                                  # sum red color
                        avgGreen += Pixels3D[math.floor(NoPixelsInRow*x + i)][math.floor(NoPixelsInCols*y + j)][1]                                                                                # sum green color
                        avgBlue  += Pixels3D[math.floor(NoPixelsInRow*x + i)][math.floor(NoPixelsInCols*y + j)][2]                                                                                 # sum blue color

                avgRed   /= TotalPixelInBlock                                                                            # avg red color
                avgBlue  /= TotalPixelInBlock                                                                            # avg green color
                avgGreen /= TotalPixelInBlock                                                                            # avg blue color
                if (y+self.y < ROWS and x + self.x < COLS):
                    grid[y+ self.y][x + self.x] = (normalize(avgRed),normalize(avgGreen),normalize(avgBlue))             # Assign color to blocks in grid


        print("RENDER TIME: "+ str((time.time_ns() - start)/1000000000) + "s")


    def renderThread(self, window, grid, num_threads):
        start = time.time_ns()
        NoPixelsInRow = math.floor(self.img.get_width() / self.w)
        NoPixelsInCols = math.floor(self.img.get_height() / self.h)
        TotalPixelInBlock = math.floor(NoPixelsInCols * NoPixelsInCols)
        ImgSurface = pygame.Surface.convert(self.img)

        print(pygame.surfarray.get_arraytypes())
        print(pygame.surfarray.get_arraytype())
        self.clear(self, grid)

        def process_blocks(start_x, end_x, start_y, end_y):
            Pixels3D = pygame.surfarray.array3d(ImgSurface)

            for x in range(start_x, end_x):
                for y in range(start_y, end_y):
                    avgRed = 0
                    avgGreen = 0
                    avgBlue = 0
                    for i in range(NoPixelsInRow):
                        for j in range(NoPixelsInCols):
                            avgRed += Pixels3D[NoPixelsInRow * x + i][NoPixelsInCols * y + j][0]  # sum red color
                            avgGreen += Pixels3D[NoPixelsInRow * x + i][NoPixelsInCols * y + j][1]  # sum green color
                            avgBlue += Pixels3D[NoPixelsInRow * x + i][NoPixelsInCols * y + j][2]
                    avgRed /= TotalPixelInBlock
                    avgBlue /= TotalPixelInBlock
                    avgGreen /= TotalPixelInBlock
                    if (y + self.y < ROWS and x + self.x < COLS):
                        grid[y + self.y][x + self.x] = (normalize(avgRed), normalize(avgGreen), normalize(avgBlue))

        block_size_x = math.ceil(self.w / num_threads)
        block_size_y = math.ceil(self.h / num_threads)
        threads = []
        for i in range(num_threads):
            start_x = i * block_size_x
            end_x = min(start_x + block_size_x, self.w)
            for j in range(num_threads):
                start_y = j * block_size_y
                end_y = min(start_y + block_size_y, self.h)
                thread = threading.Thread(target=process_blocks, args=(start_x, end_x, start_y, end_y))
                thread.start()
                threads.append(thread)

        for thread in threads:
            thread.join()

        print("RENDER TIME: " + str((time.time_ns() - start) / 1000000000) + "s")



    def renderOpenCL(self,window,grid):
    # This algorithm takes the average of the pixels which should be present in a block of the grid

    # Define the kernel code
        kernel_code = """
            __kernel void pixelate(
            __global const uchar4* input,
            __global uchar4* output,
            const int W,
            const int H,
            const int width,
            const int height){
            
                for (int i = 0; i < height; ++i) {
                for (int j = 0; j < width; ++j) {

                const int wStep = width / W;
                const int hStep = height / H;

                const int startX = i * wStep;
                const int endX = (i + 1) * wStep;
                const int startY = j * hStep;
                const int endY = (j + 1) * hStep;

                int rSum = 0, gSum = 0, bSum = 0;
                int count = 0;

                for (int x = startX; x < endX; ++x) {
                    for (int y = startY; y < endY; ++y) {
                        const int index = j * height + i;
                        const uchar4 pixel = input[index];

                        rSum += pixel.x;
                        gSum += pixel.y;
                        bSum += pixel.z;

                        count++;
                    }
                }
                const int pixelIndex = j * H + i;
                uchar4 avgPixel = (uchar4)(rSum / count, gSum / count, bSum / count, 255);
                output[pixelIndex] = avgPixel;
            }
            }}
        """

        def pixelate_image(image_array, W, H):
            # Convert image array to numpy array
            image_np = np.array(image_array, dtype=np.uint8)

            # Reshape the image array to a flat array of pixels
            flat_image = image_np.reshape(-1, 3)

            # Initialize OpenCL context
            ctx = cl.create_some_context()
            queue = cl.CommandQueue(ctx)

            # Create input and output buffers
            mf = cl.mem_flags
            input_buffer = cl.Buffer(ctx, mf.READ_ONLY | mf.COPY_HOST_PTR, hostbuf=flat_image)
            output_buffer = cl.Buffer(ctx, mf.WRITE_ONLY, size=flat_image.nbytes)

            # Compile the kernel code and create the kernel
            prg = cl.Program(ctx, kernel_code).build()
            kernel = prg.pixelate

            # Get the image dimensions
            width, height, _ = image_np.shape

            # Convert W and H to np.int32
            W = np.int32(W)
            H = np.int32(H)
            width = np.int32(width)
            height = np.int32(height)

            # Execute the kernel
            kernel_args = (input_buffer, output_buffer, W, H, width, height)
            kernel(queue, (W, H), None, *kernel_args)

            # Read the output buffer
            output_image = np.empty_like(flat_image)
            cl.enqueue_copy(queue, output_image, output_buffer)

            # Reshape the output image to the original shape
            output_image = output_image.reshape(image_np.shape)

            return output_image.tolist()
        input_image = [
            [(255, 0, 0), (0, 255, 0), (0, 0, 255)],
            [(0, 0, 255), (255, 0, 0), (0, 255, 0)],
            [(0, 255, 0), (0, 0, 255), (255, 0, 0)]
        ]

        W = 2
        H = 2

        output_image = pixelate_image(input_image, W, H)
        print(output_image)

        Pixels3D = pygame.surfarray.array3d(self.img)
        pixelated = pixelate_image(Pixels3D, 40, 40)

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                grid[i][j] = pixelated[i][j]


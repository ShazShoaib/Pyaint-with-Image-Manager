# Shaz Shoaib 21554
# Shehzad Khuwaja 22852
# Agha Kazim 23025
# Mubeen Anwar 23022
# Mohammad Mohsin 22837

from Code.settings import *
from Code.ImageManager import *
from Code.button import *

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH + SECOND_TOOLBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Pyaint")
STATE = "COLOR"
Change = False


def init_grid(rows, columns, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(columns):  # use _ when variable is not required
            grid[i].append(color)
    return grid


def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))


def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5, HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "FillBucket":
                text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Brush":
                text_surface = pos_font.render("Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Change":
                text_surface = pos_font.render("Swap Toolbar", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            r, g, b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)

            win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))

        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10, HEIGHT - TOOLBAR_HEIGHT))
                break


def draw(win, grid, buttons, imageManager, isImage):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    draw_brush_widths(win)
    draw_mouse_position_text(win)

    if isImage:  # checks if there is a change in the image
        if FAST_RENDER:
            ImgMan.renderFast(ImgMan,WIN,grid)          # renders the image using a quick algo with potentially reduced accuracy (CPU)
        elif GPU_ACCELERATION:
            ImgMan.renderOpenCL(ImgMan, WIN, grid)      # renders the image using OpenCL
        else:
            ImgMan.renderSurf(ImgMan,WIN,grid)          # renders the image using CPU
        isImage = False                                 # there is now no change in the image

    pygame.display.update()


def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),
        Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse"),
        Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, None, "ellipse")
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (BRUSH_SIZE == 2 and button.width == size_medium) or (
                BRUSH_SIZE == 3 and button.width == size_large)):
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height),
                            border_width)  # border


def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= ROWS:
        raise IndexError
    return row, col


def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        grid[row][col] = drawing_color
    else:  # for values greater than 1
        r = row - BRUSH_SIZE + 1
        c = col - BRUSH_SIZE + 1

        for i in range(BRUSH_SIZE * 2 - 1):
            for j in range(BRUSH_SIZE * 2 - 1):
                if r + i < 0 or c + j < 0 or r + i >= ROWS or c + j >= COLS:
                    continue
                grid[r + i][c + j] = drawing_color

            # Checks whether the coordinated are within the canvas


def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1


def fill_bucket(row, col, color):
    # Visiting array
    vis = [[0 for i in range(101)] for j in range(101)]

    # Creating queue for bfs
    obj = []

    # Pushing pair of {x, y}
    obj.append([row, col])

    # Marking {x, y} as visited
    vis[row][col] = 1

    # Until queue is empty
    while len(obj) > 0:

        # Extracting front pair
        coord = obj[0]
        x = coord[0]
        y = coord[1]
        preColor = grid[x][y]

        grid[x][y] = color

        # Popping front pair of queue
        obj.pop(0)

        # For Upside Pixel or Cell
        if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
            obj.append([x + 1, y])
            vis[x + 1][y] = 1

        # For Downside Pixel or Cell
        if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
            obj.append([x - 1, y])
            vis[x - 1][y] = 1

        # For Right side Pixel or Cell
        if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
            obj.append([x, y + 1])
            vis[x][y + 1] = 1

        # For Left side Pixel or Cell
        if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
            obj.append([x, y - 1])
            vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_width = 40
button_height = 40
button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT / 2 + 1
button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH / 2
brush_widths = [
    Button(rtb_x - size_small / 2, 480, size_small, size_small, drawing_color, None, "ellipse"),
    Button(rtb_x - size_medium / 2, 510, size_medium, size_medium, drawing_color, None, "ellipse"),
    Button(rtb_x - size_large / 2, 550, size_large, size_large, drawing_color, None, "ellipse")
]

button_y_top_row = HEIGHT - TOOLBAR_HEIGHT / 2 - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT / 2 + 1
button_space = 42

# Adding Buttons
buttons = []

for i in range(int(len(COLORS) / 2)):
    buttons.append(Button(100 + button_space * i, button_y_top_row, button_width, button_height, COLORS[i]))

for i in range(int(len(COLORS) / 2)):
    buttons.append(
        Button(100 + button_space * i, button_y_bot_row, button_width, button_height, COLORS[i + int(len(COLORS) / 2)]))

# Right toolbar buttonst
# need to add change toolbar button.
for i in range(10):
    if i == 0:
        buttons.append(Button(HEIGHT - 2 * button_width, (i * button_height) + 5, button_width, button_height, WHITE,
                              name="Change"))  # Change toolbar buttons
    else:
        buttons.append(Button(HEIGHT - 2 * button_width, (i * button_height) + 5, button_width, button_height, WHITE,
                              "B" + str(i - 1), BLACK))  # append tools

buttons.append(
    Button(WIDTH - button_space, button_y_top_row, button_width, button_height, WHITE, "Erase", BLACK))  # Erase Button
buttons.append(
    Button(WIDTH - button_space, button_y_bot_row, button_width, button_height, WHITE, "Clear", BLACK))  # Clear Button
buttons.append(
    Button(WIDTH - 3 * button_space + 5, button_y_top_row, button_width - 5, button_height - 5, name="FillBucket",
           image_url="assets/paint-bucket.png"))  # FillBucket
buttons.append(
    Button(WIDTH - 3 * button_space + 45, button_y_top_row, button_width - 5, button_height - 5, name="Brush",
           image_url="assets/paint-brush.png"))  # Brush

# New Buttons Added for Image Manipulation
buttons.append(Button(rtb_x - size_large / 2 + 50, 5, size_small, size_medium, color=(150, 150, 150), text='',
                      name="GS"))  # Greyscale the Image
buttons.append(
    Button(rtb_x - size_large / 2 + 50 + size_small, 5, size_small, size_medium, color=(250, 20, 20), text='',
           name="Red"))  # Apply Red Filter
buttons.append(
    Button(rtb_x - size_large / 2 + 50 + size_small * 2, 5, size_small, size_medium, color=(20, 250, 20), text='',
           name="Green"))  # Apply Green Filter
buttons.append(
    Button(rtb_x - size_large / 2 + 50 + size_small * 3, 5, size_small, size_medium, color=(20, 20, 250), text='',
           name="Blue"))  # Apply Blue Filter
buttons.append(Button(rtb_x - size_large / 2 + 50, 50, size_large, size_large, color=(150, 200, 100), text='ROT',
                      name="rotate"))  # Rotate the Image 90 degrees
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large, size_large, size_large, color=(150, 200, 100), text='H flip',
           name="H flip"))  # Horizontally Flip the Image
buttons.append(Button(rtb_x - size_large / 2 + 50, 50 + size_large * 2, size_large, size_large, color=(150, 200, 100),
                      text='V flip', name="V flip"))  # Vertically Flip the Image
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 3, size_small, size_large, color=(150, 200, 100), text='L',
           name="MLeft"))  # Move the Image 1 step to the Left
buttons.append(Button(rtb_x - size_large / 2 + 50 + size_small * 3, 50 + size_large * 3, size_small, size_large,
                      color=(150, 200, 100), text='R', name="MRight"))  # Move the Image 1 step to the Right
buttons.append(
    Button(rtb_x - size_large / 2 + 50 + size_small, 50 + size_large * 3, size_large, size_small, color=(150, 200, 100),
           text='MU', name="MUp"))  # Move the Image 1 step Upwards
buttons.append(
    Button(rtb_x - size_large / 2 + 50 + size_small, 50 + size_large * 3 + size_small, size_large, size_small,
           color=(150, 200, 100), text='MD', name="MDown"))  # Move the Image 1 step Downwards
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 4, size_large, size_large, color=(150, 200, 100), text='HU',
           name="HUp"))  # Increase the Height by 1
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 5, size_large, size_large, color=(150, 200, 100), text='HD',
           name="HDown"))  # Decrease the Height by 1
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 6, size_large, size_large, color=(150, 200, 100), text='WU',
           name="WUp"))  # Increase the Width by 1
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 7, size_large, size_large, color=(150, 200, 100), text='WD',
           name="WDown"))  # Decrease the Width by 1
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 8, size_large, size_large, color=(200, 0, 0), text='X',
           name="remove"))  # Remove the image
buttons.append(
    Button(rtb_x - size_large / 2 + 50, 50 + size_large * 9, size_large, size_large, color=(100, 100, 250), text='Load',
           name="upload"))  # Load a Image
buttons.append(Button(rtb_x - size_large / 2 + 50, 50 + size_large * 10, size_large, size_large, color=(100, 100, 250),
                      text='QSave', name="QSave"))  # Quick Screenshot of the Grid
buttons.append(Button(rtb_x - size_large / 2 + 50, 50 + size_large * 11, size_large, size_large, color=(100, 100, 250),
                      text='Save', name="SaveAs"))  # Screenshot of the Grid

draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT / 2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

ImgMan = ImageManager
ImgMan.__init__(ImgMan)
isImage = False

base_font = pygame.font.Font(None, 32)
user_text = 'stadium.bmp'
input_rect = pygame.Rect(200, 200, 140, 32)
color = pygame.Color('chartreuse4')

text = False
upload = False
save = False
savedelay = False
while run:
    clock.tick(FPS)  # limiting FPS to 60 or any other value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # if user closed the program
            run = False

        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)

                if STATE == "COLOR":
                    paint_using_brush(row, col, BRUSH_SIZE)

                elif STATE == "FILL":
                    fill_bucket(row, col, drawing_color)

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                        # New Buttons for Image Management START here
                    if button.name == "upload":
                        ImgMan.AutoImage(ImgMan)
                        text = True
                        user_text = "stadium.bmp"
                        isImage = True
                        upload = True
                        break

                    if button.name == "QSave":
                        WINcrop = pygame.Rect(0, 0, WIDTH, HEIGHT - TOOLBAR_HEIGHT)
                        ImgMan.quicksave(ImgMan, WIN.subsurface(WINcrop))
                        break

                    if button.name == "SaveAs":
                        text = True
                        save = True

                    if button.name == "remove":
                        isImage = False
                        break

                    if button.name == "rotate":
                        isImage = True
                        ImgMan.rotate(ImgMan, 90)
                        break

                    if button.name == "H flip":
                        isImage = True
                        ImgMan.flipHorizontal(ImgMan)
                        break

                    if button.name == "V flip":
                        isImage = True
                        ImgMan.flipVertical(ImgMan)
                        break

                    if button.name == "MLeft":
                        isImage = True
                        ImgMan.setX(ImgMan, ImgMan.x - 1)
                        break

                    if button.name == "MRight":
                        isImage = True
                        ImgMan.setX(ImgMan, ImgMan.x + 1)
                        break

                    if button.name == "MUp":
                        isImage = True
                        ImgMan.setY(ImgMan, ImgMan.y - 1)
                        break

                    if button.name == "MDown":
                        isImage = True
                        ImgMan.setY(ImgMan, ImgMan.y + 1)
                        break

                    if button.name == "WUp":
                        isImage = True
                        ImgMan.setW(ImgMan, ImgMan.w + 1)
                        break

                    if button.name == "WDown":
                        isImage = True
                        ImgMan.setW(ImgMan, ImgMan.w - 1)
                        break

                    if button.name == "HUp":
                        isImage = True
                        ImgMan.setH(ImgMan, ImgMan.h + 1)
                        break

                    if button.name == "HDown":
                        isImage = True
                        ImgMan.setH(ImgMan, ImgMan.h - 1)
                        break

                    if button.name == "GS":
                        isImage = True
                        ImgMan.applyGreyScaleFilter(ImgMan)
                        break

                    if button.name == "Red":
                        isImage = True
                        ImgMan.applyRedFilter(ImgMan)
                        break

                    if button.name == "Green":
                        isImage = True
                        ImgMan.applyGreenFilter(ImgMan)
                        break

                    if button.name == "Blue":
                        isImage = True
                        ImgMan.applyBlueFilter(ImgMan)
                        break  # New buttons for Image Management END here

                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        break

                    if button.name == "FillBucket":
                        STATE = "FILL"
                        break

                    if button.name == "Change":
                        Change = not Change
                        for i in range(10):
                            if i == 0:
                                buttons.append(Button(HEIGHT - 2 * button_width, (i * button_height) + 5, button_width,
                                                      button_height, WHITE, name="Change"))
                            else:
                                if Change == False:
                                    buttons.append(
                                        Button(HEIGHT - 2 * button_width, (i * button_height) + 5, button_width,
                                               button_height, WHITE, "B" + str(i - 1), BLACK))
                                if Change == True:
                                    buttons.append(
                                        Button(HEIGHT - 2 * button_width, (i * button_height) + 5, button_width,
                                               button_height, WHITE, "C" + str(i - 1), BLACK))
                        break

                    if button.name == "Brush":
                        STATE = "COLOR"
                        break

                    drawing_color = button.color
                    draw_button.color = drawing_color

                    break

                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    # set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"

        if savedelay:  # This saves the picture without the textbox in the way
            WINcrop = pygame.Rect(0, 0, WIDTH, HEIGHT - TOOLBAR_HEIGHT)
            ImgMan.save(ImgMan, WIN.subsurface(WINcrop), user_text)
            savedelay = False

        if text:  # handles the textbox for filename inputs
            if event.type == pygame.KEYDOWN:
                print(event.key)
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                elif event.key == pygame.K_KP_ENTER or event.key == pygame.K_RETURN:  # enter key to confirm input
                    text = False
                    # show_image = True
                    print(user_text)

                    if upload:  # loads the image in textbox
                        ImgMan.setImage(ImgMan, user_text)
                        upload = False

                    if save:  # tells the actual save to work, this way it is delayed 1 frame, removing the textbox from the screenshot
                        savedelay = True
                        save = False
                else:
                    user_text += event.unicode

            pygame.draw.rect(WIN, color, input_rect)
            text_surface = base_font.render(user_text, True, (255, 255, 255))
            WIN.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))
            input_rect.w = max(100, text_surface.get_width() + 10)
            pygame.display.flip()

        if not text:
            draw(WIN, grid, buttons, ImgMan,
                 isImage)  # modified draw, it now checks if there is a change in the image and then renders it
            isImage=False
pygame.quit()

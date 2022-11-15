from guizero import *
from sk_6812_rgbw_laggrif.Colors import *
from rpi_ws281x import *
import sk_6812_rgbw_laggrif.StopThread as StopThread

# initialisation des variables de base du programme
strip = InitStrip(255)
rgbw = [0, 0, 0, 0]
th = StopThread.RainbowThread(strip)

app = App(title='Light Manager', width=320, height=480)


def color_rgbw():
    return Color(rgbw[0], rgbw[1], rgbw[2], rgbw[3])


def color_rgb():
    return Color(rgbw[0], rgbw[1], rgbw[2])


def string_color_rgbw():
    return str(rgbw[0]) + ', ' + str(rgbw[1]) + ', ' + str(rgbw[2]) + ', ' + str(rgbw[3])


# Popup de confirmation pour quitter
def exit():
    e = app.yesno('Are you sure', 'Do you realy want to exit Light Manager?')
    if e:
        th.stop()
        Show(strip, Color(0, 0, 0, 0))
        sys.exit()


# Fonction de mise en plein ecran (avec recalcul des spacers)
def fullscreen():
    app.full_screen = not app.full_screen
    app.height = 480
    app.width = 320
    box.width = app.width
    i_box.width = app.width
    adjust()


# Fonctions liees aux threads d'animations lumineuses
def stopTh(thread):
    thread.stop()


def stopRB():
    global th
    th.stop()
    th = StopThread.RainbowThread(strip)


# Fonction de selection de la luminosite (avec un slider) 
def alpha():
    value = alpha_s.value
    strip.setBrightness(int(value))
    strip.show()
    global alpha_msg
    alpha_msg.value = value
    adjust()


def color_slider(value, pos):
    rgbw[pos] = int(value)
    Show(strip, color_rgbw())
    global msg
    msg.value = 'custom'
    global color_msg
    color_msg.value = string_color_rgbw()
    adjust()


def red_slider(value):
    color_slider(value, 0)


def green_slider(value):
    color_slider(value, 1)


def blue_slider(value):
    color_slider(value, 2)


def white_slider(value):
    color_slider(value, 3)


# Fonctions des boutons de couleurs predefinies
def button(text):
    stopRB()
    Show(strip, color_rgbw())
    global msg
    msg.value = text
    global color_msg
    color_msg.value = string_color_rgbw()
    adjust()


def white():
    global rgbw
    rgbw = [0, 0, 40, 255]
    button("white")


def blue():
    global rgbw
    rgbw = [0, 0, 255, 0]
    button("blue")


def green():
    global rgbw
    rgbw = [0, 255, 0, 0]
    button("green")


def red():
    global rgbw
    rgbw = [255, 0, 0, 0]
    button("red")


def black():
    global rgbw
    rgbw = [0, 0, 0, 0]
    button('black')


def rb():
    global th
    th.start()
    global msg
    msg.value = 'rainbow'
    global color_msg
    color_msg.value = '----'
    adjust()
    color_msg.bg = app.bg
    color_msg.text_color = (0, 0, 0)


def adjust():
    global i_spacer_middle
    i_spacer_middle.width = i_box.width - 9.7 * (c_msg.width + color_msg.width + a_msg.width + alpha_msg.width)
    global spacer
    spacer.width = box.width - 12 * (msg.width + exit_b.width)
    col_bg = []
    col_txt = []
    for n in rgbw[0: -1]:
        col_bg += [max(0, min(n + rgbw[3], 255))]
        col_txt += [max(0, min(255 - (n + rgbw[3]), 255))]
    color_msg.bg = col_bg
    color_msg.text_color = col_txt


# Barre de menu (pour mettre en plein ecran)
menubar = MenuBar(app,
                  toplevel=['View'],
                  options=[
                      [['Fullscreen', fullscreen]]
                  ])

# Message indiquant la couleur et bouton exit
box = Box(app, layout='grid', height=50, width=app.width)

msg = Text(box, text='bonjour', grid=[0, 0], align='left', width=7)
exit_b = PushButton(box, command=exit, text='exit', grid=[2, 0], align='right', width=3)

spacer = Box(box, width=0, height='fill', grid=[1, 0])
spacer.width = box.width - 12 * (msg.width + exit_b.width)

# couleur rgbw et luminosite
i_box = Box(app, layout='grid', width=app.width, height=24)

c_msg = Text(i_box, text='rgbw:', grid=[0, 0], width=5)
color_msg = Text(i_box, text='0, 0, 0, 0', grid=[2, 0], width=15)
a_msg = Text(i_box, text='alpha:', grid=[4, 0], width=5)
alpha_msg = Text(i_box, text='0', grid=[6, 0], width=3)

i_spacer_middle = Box(i_box, grid=[3, 0], width=0, height='fill')
i_spacer_middle.width = i_box.width - 9.7 * (c_msg.width + color_msg.width + a_msg.width + alpha_msg.width)
print(c_msg.text_size)

# Slider de selection de la luminosite
alpha_s = Slider(app, command=alpha, start=0, end=255, width='fill')

red_s = Slider(app, command=red_slider, start=0, end=255, width='fill')

green_s = Slider(app, command=green_slider, start=0, end=255, width='fill')

blue_s = Slider(app, command=blue_slider, start=0, end=255, width='fill')

white_s = Slider(app, command=white_slider, start=0, end=255, width='fill')

# Boutons pour les couleurs predefinies
b_row1 = Box(app, layout='grid', width=0, height=0)
b_row2 = Box(app, layout='grid', width=0, height=0)
b_row3 = Box(app, layout='grid', width=0, height=0)

white_b = PushButton(b_row1, command=white, text='white', grid=[0, 1])
blue_b = PushButton(b_row2, command=blue, text='blue', grid=[4, 0])
green_b = PushButton(b_row2, command=green, text='green', grid=[2, 0])
red_b = PushButton(b_row2, command=red, text='red', grid=[0, 0])
black_b = PushButton(b_row1, command=black, text='black', grid=[2, 1])
rainbow_b = PushButton(b_row3, command=rb, text='rainbow', grid=[0, 0])

b_spacer_h1 = Box(b_row1, grid=[1, 0], width=1, height='fill')
b_spacer_h2 = Box(b_row2, grid=[1, 0], width=1, height='fill')
b_spacer_h3 = Box(b_row2, grid=[3, 0], width=1, height='fill')
b_spacer_v1 = Box(b_row1, grid=[0, 0], width='fill', height=20)
b_spacer_v1 = Box(b_row1, grid=[0, 2], width='fill', height=2)
b_spacer_v2 = Box(b_row2, grid=[0, 2], width='fill', height=2)

# Affiche l'application
adjust()
alpha()
app.display()

# Lorsque l'application est fermee, quitte les threads en cours et arrete le programme
th.stop()
Show(strip, Color(0, 0, 0, 0))
sys.exit()

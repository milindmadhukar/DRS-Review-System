import tkinter
import PIL.Image, PIL.ImageTk
import cv2
from functools import partial
import threading
import imutils
import time
import sys
import os
import re
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from math import floor

WIDHT = 650
HEIGHT = 590

stream = cv2.VideoCapture(" ")

def openFile():
    file = askopenfilename(defaultextension=".mp4",filetypes=[("Video File(.mp4)","*.mp4")])
    if file == "":
        file = None
        
    else:
        f = open(file, "r")
        
        filepath.set(f.name)
        f.close()

    try:
        global stream
        stream = cv2.VideoCapture(f"{filepath.get()}")
        showinfo("DRS System","Video Loaded Sucessfully, make the correct decision!")


    except Exception as e:
        showinfo("Error Occured")
        exit()

    
        

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS

    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path,relative_path)

def seekVideo(a,b, *args):

    scrollbar.set(b,b)
    scrollbarPercent = scrollbar.get()[0]
    vid_fps = floor(int(stream.get(cv2.CAP_PROP_FPS)))
    totalFrames = int(stream.get(cv2.CAP_PROP_FRAME_COUNT))

    duration = totalFrames/vid_fps
    currentDuration = duration * scrollbarPercent
    currentFrame = totalFrames *  scrollbarPercent
    stream.set(cv2.CAP_PROP_POS_FRAMES, currentFrame)
    grabbed, frame = stream.read()
    frame = imutils.resize(frame, width= WIDHT, height= 368)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,anchor= tkinter.NW, image= frame)
    canvas.create_text(150,40,fill="yellow", font= "Times 24 bold", text= "Decision Pending")
    canvas.create_text(550,40,fill="yellow", font= "Times 24 bold", text= f"{str(floor(currentDuration))} secs")



def play(speed):

    frame1 = stream.get(cv2.CAP_PROP_POS_FRAMES)
    stream.set(cv2.CAP_PROP_POS_FRAMES, frame1 + speed)

    grabbed, frame = stream.read()
    frame = imutils.resize(frame, width= WIDHT, height= 368)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,anchor= tkinter.NW, image= frame)

    canvas.create_text(150,40,fill="yellow", font= "Times 24 bold", text= "Decision Pending")


def out():
    thread = threading.Thread(target=pending, args=("out",))
    thread.daemon = 1
    thread.start()
    print("Player is out")

def pending(decision):
    # Display decision pending image
    frame = cv2.cvtColor(cv2.imread(resource_path("decision pending.png")), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = WIDHT, height = 368)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,anchor= tkinter.NW, image= frame)
    time.sleep(2)

    frame = cv2.cvtColor(cv2.imread(resource_path("sponser.png")), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = WIDHT, height = 368)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,anchor= tkinter.NW, image= frame)

    time.sleep(2.5)

    if(decision == "out"):
        decisionImg = "out"
    else:
        decisionImg = "not out"

    frame = cv2.cvtColor(cv2.imread(resource_path(f"{decisionImg}.png")), cv2.COLOR_BGR2RGB)
    frame = imutils.resize(frame, width = WIDHT, height = 368)
    frame = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(frame))
    canvas.image = frame
    canvas.create_image(0,0,anchor= tkinter.NW, image= frame)


def notOut():
    thread = threading.Thread(target= pending, args=("not out",))
    thread.daemon = 1
    thread.start()

window = tkinter.Tk()

window.title("DRS Review System")
window.geometry(f"{WIDHT}x{HEIGHT}")
cv_img = cv2.cvtColor(cv2.imread(resource_path("welcome.png")),cv2.COLOR_BGR2RGB)
canvas = tkinter.Canvas(window, width= WIDHT, height= 368)
welcome = PIL.ImageTk.PhotoImage(image= PIL.Image.fromarray(cv_img))
welcome_canvas = canvas.create_image(0,0,anchor= tkinter.NW, image= welcome)
canvas.pack()

scrollbar = tkinter.Scrollbar(window,orient= tkinter.HORIZONTAL)
scrollbar.pack(fill = tkinter.X)
scrollbar.config(command= seekVideo)

# tempCanvas = tkinter.Canvas(window,width = 0, height =0, xscrollcommand = scrollbar.set)
# tempCanvas.pack()
# scrollbar.config(command=tempCanvas.xview)

filepath = tkinter.StringVar()
fileVal = tkinter.Entry(window, textvariable= filepath).pack(fill = tkinter.X)

btn = tkinter.Button(window, text= "Select Video File", width = 50, command = openFile)
btn.pack(fill= tkinter.X)

# buttons to control
btn = tkinter.Button(window, text= "<< Previous(fast)", width = 50, command = partial(play, -25))
btn.pack(fill= tkinter.X)

btn = tkinter.Button(window, text= "Next(fast) >>", width = 50, command = partial(play, 25))
btn.pack(fill= tkinter.X)

btn = tkinter.Button(window, text= "<< Previous(slow)", width = 50, command = partial(play, -2))
btn.pack(fill= tkinter.X)

btn = tkinter.Button(window, text= "Next(slow) >>", width = 50, command = partial(play, 2))
btn.pack(fill= tkinter.X)

btn = tkinter.Button(window, text= "Give Decision Out!", width = 50, command = out)
btn.pack(fill= tkinter.X)

btn = tkinter.Button(window, text= "Give Decision Not Out!" , width = 50, command = notOut)
btn.pack(fill= tkinter.X)


window.mainloop()


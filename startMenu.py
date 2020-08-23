import tkinter as tk
import os
from PIL import ImageTk, Image
from tkinter import messagebox 


HEIGHT = 540
WIDTH = 960
mapping = ""
icondir = "./sprites/camico.ico"

root = tk.Tk()
root.title('Social-Distance Detector (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
root.iconbitmap(icondir)

def exitApp():
   tk.messagebox.showinfo( "(づ｡◕‿‿◕｡)づ", "Thank You!")
   root.destroy
   root.quit()

def closeButton(place,tab):
    closbutton = tk.Button(place, bg='#14191E', width=15, height=1, text="Back", fg='white', command=tab.destroy)
    closbutton.place(relx=0.8, rely=0.9)

def openAbout():
    top = tk.Toplevel()
    top.title('About Us (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    top.iconbitmap(icondir)
    canvas = tk.Canvas(top, height=HEIGHT, width = WIDTH)
    canvas.pack()

    frame = tk.Frame(top, bg='#14191E')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text='Social-Distance Detector', bg='#14191E', fg='white', font=("Bebasneue-regular",34))
    label.place(relx=0.05, rely=0.05)

    label = tk.Label(frame, text='Enter Image Directory:', bg='#14191E', fg='white', font=("Bebasneue-regular",18))
    label.place(relx=0.0525, rely=0.2)

    entry = tk.Entry(frame, bg='#252e38', fg='white', font=("segouil"))
    entry.place(relx=0.0525, rely=0.27, relwidth=0.5, relheight=0.06)

    button = tk.Button(frame, text="GO", bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)
    
    button = tk.Button(frame, text="GO", bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)

    closeButton(frame,top)
   

    top.resizable(0, 0)

def openImage():
    top = tk.Toplevel()
    top.title('Image (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    top.iconbitmap(icondir)
    canvas = tk.Canvas(top, height=HEIGHT, width = WIDTH)
    canvas.pack()

    frame = tk.Frame(top, bg='#14191E')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text='Social-Distance Detector', bg='#14191E', fg='white', font=("Bebasneue-regular",34))
    label.place(relx=0.05, rely=0.05)

    label = tk.Label(frame, text='Enter Image Directory:', bg='#14191E', fg='white', font=("Bebasneue-regular",18))
    label.place(relx=0.0525, rely=0.2)

    entry = tk.Entry(frame, bg='#252e38', fg='white', font=("segouil"))
    entry.place(relx=0.0525, rely=0.27, relwidth=0.5, relheight=0.06)

    button = tk.Button(frame, text="GO", bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)
    
    button = tk.Button(frame, text="GO", command=eventClick, bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)

    closeButton(frame,top)

    top.resizable(0, 0)

def openVideo():
    top = tk.Toplevel()
    top.title('Video (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    top.iconbitmap(icondir)
    canvas = tk.Canvas(top, height=HEIGHT, width = WIDTH)
    canvas.pack()

    frame = tk.Frame(top, bg='#14191E')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text='Social-Distance Detector', bg='#14191E', fg='white', font=("Bebasneue-regular",34))
    label.place(relx=0.05, rely=0.05)

    label = tk.Label(frame, text='Enter Video Directory:', bg='#14191E', fg='white', font=("Bebasneue-regular",18))
    label.place(relx=0.0525, rely=0.2)

    entry = tk.Entry(frame, bg='#252e38', fg='white', font=("segouil"))
    entry.place(relx=0.0525, rely=0.27, relwidth=0.5, relheight=0.06)

    button = tk.Button(frame, text="GO", command=eventClick, bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)
    
    mapping = entry

    closeButton(frame,top)

    top.resizable(0, 0)

def openCam():
    top = tk.Toplevel()
    top.title('Live Cam (ﾉ◕ヮ◕)ﾉ*:･ﾟ✧')
    top.iconbitmap(icondir)
    canvas = tk.Canvas(top, height=HEIGHT, width = WIDTH)
    canvas.pack()

    frame = tk.Frame(top, bg='#14191E')
    frame.place(relwidth=1, relheight=1)

    label = tk.Label(frame, text='Social-Distance Detector', bg='#14191E', fg='white', font=("Bebasneue-regular",34))
    label.place(relx=0.05, rely=0.05)

    label = tk.Label(frame, text='Enter Image Directory:', bg='#14191E', fg='white', font=("Bebasneue-regular",18))
    label.place(relx=0.0525, rely=0.2)

    entry = tk.Entry(frame, bg='#252e38', fg='white', font=("segouil"))
    entry.place(relx=0.0525, rely=0.27, relwidth=0.5, relheight=0.06)

    button = tk.Button(frame, text="GO", command=eventClick, bg='#14191E', fg='white')
    button.place(relx=0.555, rely=0.27, relwidth=0.062, relheight=0.062)
    
    mapping = entry


    closeButton(frame,top)

    top.resizable(0, 0)
    

def eventClick():
    param = mapping
    os.chdir('D:/projectAI2/sdd')
    runcmd(param)

def runcmd(directory):
	os.system("python sdd_main.py --input " + directory + "  --output outputtt.avi --birdview birdview.avi")




about = tk.PhotoImage(file='./sprites/about.png')
about = about.subsample(10,10)

exit = tk.PhotoImage(file='./sprites/exit.png')
exit = exit.subsample(10,10)

image = tk.PhotoImage(file='./sprites/image.png')
image = image.subsample(10,10)

video = tk.PhotoImage(file='./sprites/video.png')
video = video.subsample(10,10)

livecam = tk.PhotoImage(file='./sprites/livecam.png')
livecam= livecam.subsample(10,10)


canvas = tk.Canvas(root, height=HEIGHT, width = WIDTH)
canvas.pack()

frame = tk.Frame(root, bg='#14191E')
frame.place(relwidth=1, relheight=1)

label = tk.Label(frame, text='Social-Distance Detector', bg='#14191E', fg='white', font=("Bebasneue-regular",34))
label.place(relx=0.05, rely=0.05)

button = tk.Button(frame, bg='#14191E', width=150, height=150, image=about, command = openAbout)
button.place(relx=0.25, rely=0.27)
button = tk.Button(frame, bg='#14191E', width=300, height=150, image=livecam, command = openCam)
button.place(relx=0.411, rely=0.27)
button = tk.Button(frame, bg='#14191E', width=150, height=150, image=exit, command = exitApp)
button.place(relx=0.25, rely=0.555)
button = tk.Button(frame, bg='#14191E', width=150, height=150, image=image, command = openImage)
button.place(relx=0.411, rely=0.555)
button = tk.Button(frame, bg='#14191E', width=150, height=150, image=video, command = openVideo)
button.place(relx=0.567, rely=0.555)

root.resizable(0, 0)

root.mainloop()
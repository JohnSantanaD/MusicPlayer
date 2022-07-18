#Modules
from tkinter import ACTIVE, END, Button, Label, StringVar, Tk, filedialog, ttk, Frame, PhotoImage, Listbox
from tkinter.font import BOLD, ITALIC
from pygame import mixer
import mutagen
import eyed3
import os
import random

mixer.init()
#Global Variables
global paused, playing,position,total,openfile,song,looping,mute,randoms,volumen

total = 0
position = 0
volumen = 0
song = ""
paused = False
playing = False
openfile = False
looping = False
randoms = False
mute = False

#Functions
def openFile():
    global openfile,total

    directory = filedialog.askdirectory()
    for file ,dir,songs in os.walk(directory):
        for song in songs:
            if os.path.splitext(song)[1] == '.mp3':
                song = song.replace(".mp3", "")
                path = (file + '/' + song).replace('\\', '/')
                screenListMusic.insert(END, path)
                openfile = True
    screenListMusic.select_set(position)
    total = screenListMusic.size()

def songName(song):

    audioInfo = eyed3.load(song)
    songname = audioInfo.tag.title
    name['text'] = songname

def startMusic(selectSong):
    global total, position, playing,song,paused

    song = screenListMusic.get(selectSong)
    song = f'{song}.mp3'

    mixer.music.unload()
    mixer.music.load(song)
    mixer.music.play()
    songName(song)

    total = screenListMusic.size()
    position = (screenListMusic.curselection())
    position = int(position[0])
    positionSong['text'] = ((position+1), "/", total)

    btnPlay['image'] = imgPause
    playing = True
    paused = False

    root.after(100, timeCurrent)

def pause(is_paused):
	global paused
	paused = is_paused

	if paused == True:
		mixer.music.unpause()
		paused = False
		btnPlay['image'] = imgPause
	else:
		mixer.music.pause()
		paused = True
		btnPlay['image'] = imgPlay

def play(is_playing):
    global playing
    playing = is_playing

    if openfile == True:
        if playing == False:
            startMusic(ACTIVE)
        else:
            pause(paused)

def next():

    if openfile == True:

        if (position+1) != total and randoms == False:
            next = screenListMusic.curselection()
            next = next[0]+1

            screenListMusic.selection_clear(0, END)
            screenListMusic.activate(next)
            screenListMusic.selection_set(next, None)
            startMusic(next)
        else:
            shuffleSong()

def previous():

    if openfile == True:
        if position != 0:
            back = screenListMusic.curselection()
            back = back[0]-1

            screenListMusic.selection_clear(0, END)
            screenListMusic.activate(back)
            screenListMusic.selection_set(back, None)
            startMusic(back)

def doubleclick(event):
    song = screenListMusic.curselection()
    startMusic(song)

def changeVolume(event):
    global volumen,mute

    volumen = volume.get()
    levelVolume['text'] = int(volumen)
    mixer.music.set_volume(volumen / 10)

    if int(volumen) == 0:
        btnMute['image'] = imgMute
        mute = True
    elif int(volumen) >= 1 and int(volumen) < 4:
        btnMute['image'] = imgLow
        mute = False
    elif int(volumen) >= 4 and int(volumen) <8 :
        btnMute['image'] = imgMiddle
        mute = False
    else:
        btnMute['image'] = imgHigh
        mute = False

def muteSong(is_mute):
    global mute
    mute = is_mute

    if mute == False:
        mixer.music.set_volume(0.0)
        levelVolume['text'] = 0
        btnMute['image'] = imgMute
        mute = True
    else:
        levelVolume['text'] = int(volumen)
        mixer.music.set_volume(volumen / 10)

        if int(volumen) == 0:
            btnMute['image'] = imgMute
            mute = True
        elif int(volumen) >= 1 and int(volumen) < 4:
            btnMute['image'] = imgLow
            mute = False
        elif int(volumen) >= 4 and int(volumen) < 8:
            btnMute['image'] = imgMiddle
            mute = False
        else:
            btnMute['image'] = imgHigh
            mute = False

def shuffleSong():
    global song, position
    position = random.randrange(total)
    screenListMusic.select_clear(0, END)
    screenListMusic.activate(position)
    screenListMusic.select_set(position, None)
    song = screenListMusic.curselection()
    startMusic(song)

def timeCurrent():

    posTime = mixer.music.get_pos()
    s = posTime // 1000
    m, s = divmod(s, 60)
    m, s = int(m), int(s)
    currentTime.set(f"{m:02}:{s:02}")

    audio = mutagen.File(song)
    log = audio.info.length
    minutes, seconds = divmod(log, 60)
    minutes, seconds = int(minutes), int(seconds)
    timeTotal['text'] = str(minutes) + ":" + str(seconds)

    progressbarTime['value'] = int(int(posTime)*0.001)
    progressbarTime['maximum'] = (minutes*60 + seconds)

    if playing == True and paused == False:
        if randoms == True and looping == False:
            if mixer.music.get_busy() == False:
                shuffleSong()
        elif looping == True:
            if mixer.music.get_busy() == False:
                startMusic(ACTIVE)
        else:
            if mixer.music.get_busy() == False:
                next()

    root.after(100, timeCurrent)

def trash():
    global playing,paused,openfile

    screenListMusic.delete(0,END)
    mixer.music.stop()
    mixer.music.unload()
    currentTime.set("")
    timeTotal["text"] = ""
    name["text"] = ""
    positionSong["text"] = ""
    playing = False
    paused = False
    openfile = False
    btnPlay["image"] = imgPlay

def randomSong(is_random):
    global randoms
    randoms = is_random

    if openfile == True:
        if randoms == False:
            btnRandom['image'] = imgRandomOn
            randoms = True

        else:
            btnRandom['image'] = imgRandomOff
            randoms = False

def loops(is_loops):
    global looping
    looping = is_loops

    if openfile == True:
        if looping == False:
            btnLoop['image'] = imgLoopsOn
            looping = True
        else:
            btnLoop['image'] = imgLoopsOff
            looping = False

#Colors
white = "white"
purple = "purple"
black = "black"
pink = "pink"
blue = "blue"
yellow = "yellow"
gray = "gray"
DodgerBlue4 = "DodgerBlue4"
purpleDark = "#1E0843"
blueLight = "#7F9CFD"
greenLight = "#5CF319"

#Window
root = Tk()
root.title("MusicPlayer")
# root.iconbitmap('images\icon.ico')
root.config(bg=purpleDark)
root.resizable(0, 0)

#Frames
frameScreen = Frame(root,width=10,height=20, bg=purpleDark)
frameScreen.grid(row=0, column=0)

frameSong = Frame(root, width=10, height=20,  bg=purpleDark)
frameSong.grid(row=1, column=0, pady=8)

frameTimeSong = Frame(root, width=10, height=20, bg=purpleDark)
frameTimeSong.grid(row=2, column=0, pady=8)

frameControls = Frame(root, width=10, height=20, bg=purpleDark)
frameControls.grid(row=3, column=0, pady=8)

#Images
imgMusic = PhotoImage(file="images/music.png")
imagMusic = Label(frameScreen, image=imgMusic, bg=purpleDark)
imagMusic.grid(row=0, column=0, padx=45)

imgTrash = PhotoImage(file="images/trash.png")
imgFile = PhotoImage(file="images/folder.png")
imgPrevious = PhotoImage(file="images/back.png")
imgStop = PhotoImage(file="images/stop.png")
imgPlay = PhotoImage(file="images/play.png")
imgPause = PhotoImage(file="images/pause.png")
imgNext = PhotoImage(file="images/next.png")
imgRandomOff = PhotoImage(file="images/randomoff.png")
imgRandomOn = PhotoImage(file="images/randomon.png")
imgLoopsOff = PhotoImage(file="images/loopsoff.png")
imgLoopsOn = PhotoImage(file="images/loopson.png")
imgHigh = PhotoImage(file="images/high.png")
imgMiddle = PhotoImage(file="images/middle.png")
imgLow = PhotoImage(file="images/low.png")
imgMute = PhotoImage(file="images/mute.png")

#Listbox Screen
screenListMusic = Listbox(frameScreen, bg=purpleDark, fg=pink, font=(
	"Calibri", 10, BOLD, ITALIC), width=45, height=22, selectbackground=blueLight, selectforeground=purpleDark)
screenListMusic.bind('<Double-1>', doubleclick)
screenListMusic.grid(row=0, column=1, padx=2, pady=2)

#Label
name = Label(frameSong, width=67, bg=purpleDark, fg=yellow,
             font=("Arial", 11, BOLD, ITALIC))
name.grid(row=0, column=0, padx=2, pady=2)

positionSong = Label(frameSong,width=7, bg=purpleDark, fg=blueLight,
                     font=("Arial", 10, BOLD, ITALIC))
positionSong.grid(row=0, column=1, padx=2, pady=2)

#Progressbar Time
styleTime = ttk.Style()
styleTime.theme_use('clam')
styleTime.configure("Horizontal.TProgressbar", fg=white, background=blueLight,
                    bordercolor=gray, troughcolor=DodgerBlue4, lightcolor=black, darkcolor=blue)

currentTime = StringVar(frameTimeSong)

time = Label(frameTimeSong,textvariable=currentTime,
              bg=purpleDark, fg=greenLight,
              font = ("Arial", 10, BOLD, ITALIC))
time.grid(row=0, column=0, padx=0, pady=2)

progressbarTime = ttk.Progressbar(frameTimeSong,
                                  orient='horizontal', length=560,
                         mode='determinate', style="Horizontal.TProgressbar")
progressbarTime.grid(row=0,column=1, padx=15)

timeTotal = Label(frameTimeSong, width=3,bg=purpleDark, fg=greenLight,
             font=("Arial", 10, BOLD, ITALIC))
timeTotal.grid(row=0, column=2, padx=0, pady=2)


#Buttons
btnTrash = Button(frameControls, bg=purpleDark, image=imgTrash, command=trash)
btnTrash.grid(row=0, column=0, pady=10, padx=(10, 25))

btnFile = Button(frameControls, bg=purpleDark, image=imgFile, command=openFile)
btnFile.grid(row=0, column=1, pady=10, padx=(0, 25))

btnPrevious = Button(frameControls, bg=purpleDark,
                     image=imgPrevious, command=previous)
btnPrevious.grid(row=0, column=2, pady=10, padx=(55,2))

btnPlay = Button(frameControls, bg=purpleDark, image=imgPlay,
                 command=lambda: play(playing))
btnPlay.grid(row=0, column=3, pady=10, padx=10)

btnNext = Button(frameControls, bg=purpleDark, image=imgNext, command=next)
btnNext.grid(row=0, column=4, pady=10, padx=(2))

btnRandom = Button(frameControls, bg=purpleDark,
                   image=imgRandomOff, command=lambda: randomSong(randoms))
btnRandom.grid(row=0, column=5, pady=10, padx=(55, 10))

btnLoop = Button(frameControls, bg=purpleDark, image=imgLoopsOff,
                 command=lambda : loops(looping))
btnLoop.grid(row=0, column=6, pady=10, padx=10)

btnMute = Button(frameControls, bg=purpleDark, image=imgHigh,
                 command= lambda : muteSong(mute))
btnMute.grid(row=0, column=7, pady=10, padx=(25, 0))

#Scale Volume
volume = ttk.Scale(frameControls, to=10, from_=0, orient='horizontal')
volume.set(10)
volume['command'] = changeVolume
volume.grid(row=0, column=8, padx=0)

styleVolume = ttk.Style()
styleVolume.theme_use('clam')
styleVolume.configure("Horizontal.TScale", bordercolor=purple,
                      troughcolor=purpleDark, background=blueLight, lightcolor=black, darkcolor=black)

levelVolume = Label(frameControls, bg=purpleDark, fg=greenLight, 
                    font=("Arial", 10, BOLD, ITALIC) ,width=3)
levelVolume.grid(column=9, row=0)

root.mainloop()
#Modules
from tkinter import ACTIVE, END, Button, Label, Tk, filedialog, ttk, Frame, PhotoImage, Listbox
from tkinter.font import BOLD, ITALIC
from pygame import mixer

mixer.init()
#Global Variables
global paused, playing, position
total = 0
position = 0
paused = False
playing = False

#Functions


def openFile():
    global position

    songs = filedialog.askopenfilenames(
        initialdir="/", title="Choose a song", filetypes=(("mp3", "*.mp3"), ("all files", "*.*")))

    for song in songs:
        song = song.replace(".mp3", "")
        screenListMusic.insert(END, song)
    screenListMusic.select_set(position)


def songName(song):
    songname = (song).replace(".mp3", "")
    songname = (songname).split('/')
    songname = songname[-1]
    name['text'] = songname


def startMusic(selectSong):
    global total, position, playing

    song = screenListMusic.get(selectSong)
    song = f'{song}.mp3'
    mixer.music.load(song)
    mixer.music.play()
    songName(song)
    total = screenListMusic.size()
    position = (screenListMusic.curselection())
    position = int(position[0])
    positionSong['text'] = ((position+1), "/", total)
    btnPlay['image'] = imgPause
    playing = True


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

    if playing == False:
        startMusic(ACTIVE)
    else:
        pause(paused)


def next():
    next = screenListMusic.curselection()
    next = next[0]+1

    screenListMusic.selection_clear(0, END)
    screenListMusic.activate(next)
    screenListMusic.selection_set(next, None)
    startMusic(next)


def back():
    back = screenListMusic.curselection()
    back = back[0]-1

    screenListMusic.selection_clear(0, END)
    screenListMusic.activate(back)
    screenListMusic.selection_set(back, None)
    startMusic(back)


def doubleclick(event):
    song = screenListMusic.curselection()
    startMusic(song)


def change_volume(event):
    volumen = volume.get()
    levelVolume['text'] = int(volumen)
    mixer.music.set_volume(volumen / 10)


#Colors
purple = "purple"
black = "black"
pink = "pink"
purpleDark = "#1E0843"
blueLight = "#7F9CFD"
greenLight = "#0EF0C0"

#Window
root = Tk()
root.title("MusicPlayer")
#root.iconbitmap('icon.ico')
root.geometry("620x480")
root.config(bg=purpleDark)

#Frames
fram0 = Frame(root, bg=purpleDark)
fram0.grid(row=0, column=0)

fram1 = Frame(root, bg=purpleDark, width=20)
fram1.grid(row=1, column=0)

fram2 = Frame(root, bg=purpleDark)
fram2.grid(row=2, column=0)

fram3 = Frame(root, bg=purpleDark)
fram3.grid(row=3, column=0)

#Images
imgMusic = PhotoImage(file="music.png")
imagMusic = Label(fram0, image=imgMusic, bg=purpleDark)
imagMusic.grid(row=0, column=0, padx=0)

imgFolder = PhotoImage(file="folder.png")
imgBack = PhotoImage(file="back.png")
imgStop = PhotoImage(file="stop.png")
imgPlay = PhotoImage(file="play.png")
imgPause = PhotoImage(file="pause.png")
imgNext = PhotoImage(file="next.png")

#Screen
screenListMusic = Listbox(fram0, bg=purpleDark, fg=pink, font=(
	"Calibri", 10, BOLD, ITALIC), width=44, height=20, selectbackground=blueLight, selectforeground=purpleDark)
screenListMusic.bind('<Double-1>', doubleclick)
screenListMusic.grid(row=0, column=1, padx=45, pady=2)

#Label
name = Label(fram1, bg=purpleDark, fg="pink", font=("Arial", 11))
name.grid(row=0, column=0, padx=0, pady=2)

positionSong = Label(fram1, bg=purpleDark, fg=greenLight, font=("Arial", 9))
positionSong.grid(row=1, column=0, padx=0, pady=2)

#Buttons
btnFile = Button(fram3, bg=purpleDark, image=imgFolder, command=openFile)
btnFile.grid(row=0, column=0, pady=10, padx=10)

btnBack = Button(fram3, bg=purpleDark, image=imgBack, command=back)
btnBack.grid(row=0, column=1, pady=10, padx=10)

btnPlay = Button(fram3, bg=purpleDark, image=imgPlay,
                 command=lambda: play(playing))
btnPlay.grid(row=0, column=2, pady=10, padx=10)

btnNext = Button(fram3, bg=purpleDark, image=imgNext, command=next)
btnNext.grid(row=0, column=3, pady=10, padx=10)

#Volume
volume = ttk.Scale(fram3, to=10, from_=0, orient='horizontal')
volume.set(10)
volume['command'] = change_volume
volume.grid(row=0, column=5, padx=10)

styleVolume = ttk.Style()
styleVolume.theme_use('clam')
styleVolume.configure("Horizontal.TScale", bordercolor=blueLight,
                      troughcolor=purpleDark, background=purple, lightcolor=black, darkcolor=black)

levelVolume = Label(fram3, bg=purpleDark, fg=greenLight, width=3)
levelVolume.grid(column=6, row=0)

root.mainloop()

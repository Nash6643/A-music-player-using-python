from tkinter import *
from tkinter import filedialog
import pygame
import os

# Tk starts the program
root = Tk()
root.title("Music Player")
# This sets the size of the window
root.geometry("500x300")
# Mixer allows us to play audio
pygame.mixer.init()

# Create the menu bar
menubar = Menu(root)
root.config(menu=menubar)

# Create "Organize" menu
organisemenu = Menu(menubar, tearoff=False)
organisemenu.add_command(label="Select Folder", command=lambda: loadmusic())
menubar.add_cascade(label="Organise", menu=organisemenu)

# To load in the music
songs = []
currentsong = ""
pause = False

# Create the listbox for songs
songlist = Listbox(root, bg="blue", fg="red", width=100, height=15)

def loadmusic():
    global songs, currentsong
    # Ask the user to select a directory containing music files
    root.directory = filedialog.askdirectory()

    # Clear the existing songs list
    songs.clear()

    for song in os.listdir(root.directory):
        name, ext = os.path.splitext(song)
        if ext == ".mp3":
            songs.append(song)

    # Clear the song listbox and insert the new songs
    songlist.delete(0, END)
    for song in songs:
        songlist.insert(END, song)

    # Select the first song by default
    if songs:
        songlist.selection_set(0)
        currentsong = songs[songlist.curselection()[0]]

def playmusic():
    global currentsong, pause
    if not pause:
        pygame.mixer.music.load(os.path.join(root.directory, currentsong))
        pygame.mixer.music.play()
        pause = False
    else:
        pygame.mixer.music.unpause()
        pause = False

def pausemusic():
    global pause
    pygame.mixer.music.pause()
    pause = True

def nextmusic():
    global currentsong, pause
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(currentsong) + 1)
        currentsong = songs[songlist.curselection()[0]]
        playmusic()
    except:
        pass

def previousmusic():
    global currentsong, pause
    try:
        songlist.selection_clear(0, END)
        songlist.selection_set(songs.index(currentsong) - 1)
        currentsong = songs[songlist.curselection()[0]]
        playmusic()
    except:
        pass

# Load images for the buttons
playimages = PhotoImage(file="play.png")
pauseimages = PhotoImage(file="pause.png")
nextimages = PhotoImage(file="next.png")
previousimages = PhotoImage(file="previous.png")

# Create a frame for the buttons
controlframe = Frame(root)
controlframe.pack()

# Create buttons with the respective images
playbutton = Button(controlframe, image=playimages, borderwidth=0, command=playmusic)
pausebutton = Button(controlframe, image=pauseimages, borderwidth=0, command=pausemusic)
nextbutton = Button(controlframe, image=nextimages, borderwidth=0, command=nextmusic)
previousbutton = Button(controlframe, image=previousimages, borderwidth=0, command=previousmusic)

# Grid layout for the buttons
playbutton.grid(row=0, column=1, padx=5, pady=5)
pausebutton.grid(row=0, column=2, padx=5, pady=5)
nextbutton.grid(row=0, column=3, padx=5, pady=5)
previousbutton.grid(row=0, column=0, padx=5, pady=5)

# Pack the song list
songlist.pack()

# This executes the program and keeps the window open
root.mainloop()

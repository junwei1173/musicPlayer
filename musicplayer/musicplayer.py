import tkinter as tk
from tkinter import Listbox, PhotoImage, Frame, Button, Grid, Menu, filedialog, END, ACTIVE,Label,ANCHOR,LabelFrame
import pygame
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import os
from PIL import Image, ImageTk
import imageio

root = tk.Tk()
root.title("MUSIC PLAYER")
root.iconbitmap("wave-sound.ico")
root.geometry("1000x600")
root.resizable(False, False)
my_label = Label(root)
my_label.place(x=0,y=0,relwidth=1,relheight=1)

animated_gif_path = "hmc.gif"
animated_gif = imageio.get_reader(animated_gif_path)

first_frame = animated_gif.get_data(0)
width, height = 996, 600
resized_frames = [ImageTk.PhotoImage(Image.fromarray(frame).resize((width, height))) for frame in animated_gif]

gif_label = Label(root, image=resized_frames[0], relief='flat',bg='#a5d673')
gif_label.place(x=0, y=0)
def update_label(frame_number):
    frame_image = resized_frames[frame_number]
    gif_label.configure(image=frame_image)
    gif_label.image = frame_image  # Keep a reference to avoid garbage collection
    root.after(100, update_label, (frame_number + 2) % len(resized_frames))

update_label(1)

pygame.mixer.init()


def play_length():
    if stopped:
        return
    current_time = pygame.mixer.music.get_pos() / 1000
    accurate_time = time.strftime("%M:%S", time.gmtime(current_time))
    song = playlistWin.get(ACTIVE)
    song = f"songs/{song}.mp3"
    song_mtg = MP3(song)
    global song_length
    song_length = song_mtg.info.length
    accurate_song_length = time.strftime("%M:%S", time.gmtime(song_length))
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f'{accurate_song_length}', font="impact", fg='white')
    elif paused:
        pass
    elif int(my_slider.get()) == int(current_time):
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=int(current_time))
    else:
        slider_pos = int(song_length)
        my_slider.config(to=slider_pos, value=int(my_slider.get()))
        accurate_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))
        status_bar.config(text=f'{accurate_time}  of  {accurate_song_length}', font="impact", fg='white')
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    status_bar.after(1000,play_length)
def add_song():
    song = filedialog.askopenfilename(initialdir="songs",title="Choose A Song",filetypes=(("mp3 files","*.mp3"), ))
    song_name = os.path.basename(song)
    song_name_remove = os.path.splitext(song_name)[0]
    playlistWin.insert(END,song_name_remove)

def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="songs", title="Choose A Song",filetypes=(("mp3 files", "*.mp3"),))
    for song in songs:
        song_name = os.path.basename(song)
        song_name_remove = os.path.splitext(song_name)[0]
        playlistWin.insert(END, song_name_remove)
def play():
    global stopped
    stopped = False
    global continue_animation
    continue_animation = True
    update_label2(1)
    song = playlistWin.get(ACTIVE)
    song = f"songs/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    play_length()


global stopped
stopped = False
def stop():
    global continue_animation
    continue_animation = False
    status_bar.config(text='')
    my_slider.config(value=0)
    pygame.mixer.music.stop()
    playlistWin.select_clear(ACTIVE)
    status_bar.config(text='')
    global stopped
    stopped = True

def next_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_music = playlistWin.curselection()
    next_music = next_music[0]+1
    song = playlistWin.get(next_music)
    song = f"songs/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlistWin.select_clear(0,END)
    playlistWin.activate(next_music)
    playlistWin.selection_set(next_music,last=None)

def previous_song():
    status_bar.config(text='')
    my_slider.config(value=0)
    next_music = playlistWin.curselection()
    next_music = next_music[0]-1
    song = playlistWin.get(next_music)
    song = f"songs/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    playlistWin.select_clear(0, END)
    playlistWin.activate(next_music)
    playlistWin.selection_set(next_music, last=None)

def delete_song():
    stop()
    playlistWin.delete(ANCHOR)
    pygame.mixer.music.stop()

def delete_all_songs():
    stop()
    playlistWin.delete(0,END)
    pygame.mixer.music.stop()

global paused
paused = False
def pause(is_paused):
    global paused
    paused = is_paused
    global continue_animation
    if paused:
        pygame.mixer.music.unpause()
        continue_animation = True
        paused = False
        update_label2(1)
    else:
        pygame.mixer.music.pause()
        continue_animation = False
        paused = True

def slide(x):
    song = playlistWin.get(ACTIVE)
    song = f"songs/{song}.mp3"
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


def volume(x):
    pygame.mixer.music.set_volume(vol_slider.get())

main_frame = Frame(root,bg="#a5d673")
main_frame.pack(pady=100)


#create playlist window
playlistWin = Listbox(main_frame, bg="#9cd1f0", fg="white", width=50,selectforeground="white",selectbackground="#74c1ed",font=("Impact", 13),relief='flat')
playlistWin.grid(row=0,column=0)

#player control button images
back_button_img = PhotoImage(file="back.png")
forward_button_img = PhotoImage(file="forward.png")
play_button_img = PhotoImage(file="play-button.png")
pause_button_img = PhotoImage(file="pause.png")
stop_button_img = PhotoImage(file="stop-button.png")

#player button frame
buttons_frame = Frame(main_frame,bg='#a5d673')
buttons_frame.grid(row=1,column=0,pady=0)

#volume frame
vol_frame = LabelFrame(main_frame,text='Volume',font='impact',bg='#a5d673',relief='flat',fg="white")
vol_frame.grid(row=0,column=1)
#player control buttons
back_button = Button(buttons_frame,image=back_button_img,borderwidth=0,command=previous_song)
forward_button = Button(buttons_frame,image=forward_button_img,borderwidth=0,command=next_song)
play_button = Button(buttons_frame,image=play_button_img,borderwidth=0,command=play)
pause_button = Button(buttons_frame,image=pause_button_img,borderwidth=0,command=lambda:pause(paused))
stop_button = Button(buttons_frame,image=stop_button_img,borderwidth=0,command=stop)

back_button.grid(row=0,column=0,padx=0)
forward_button.grid(row=0,column=1,padx=0)
play_button.grid(row=0,column=2,padx=0)
pause_button.grid(row=0,column=3,padx=0)
stop_button.grid(row=0,column=4,padx=0)

animated_gif_path2 = "turtle.gif"
animated_gif2 = imageio.get_reader(animated_gif_path2)

first_frame2 = animated_gif2.get_data(0)
width2, height2 = 90, 80
resized_frames2 = [ImageTk.PhotoImage(Image.fromarray(frame).resize((width2, height2))) for frame in animated_gif2]
gif_label2 = Label(root, image=resized_frames2[0],relief='flat',bg="#a5d673")
gif_label2.place(x=660, y=337)

continue_animation = True
def update_label2(frame_number):
    if not continue_animation:
        return
    frame_image = resized_frames2[frame_number]
    gif_label2.configure(image=frame_image, bg="#a5d673")
    gif_label2.image = frame_image
    root.after(100, update_label2, (frame_number + 1) % len(resized_frames2))



#menu
my_menu = Menu(root)
root.config(menu=my_menu)
#add song menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Menu",menu=add_song_menu)
add_song_menu.add_command(label="Add a Song to Playlist",command=add_song)
#add many songs
add_song_menu.add_command(label="Add Multiple Songs to Playlist",command=add_many_songs)

#remove songs
remove_songs = Menu(my_menu)
my_menu.add_cascade(label="Remove",menu=remove_songs)
remove_songs.add_command(label="Delete a Song From Playlist",command=delete_song)
remove_songs.add_command(label="Delete All Song From Playlist",command=delete_all_songs)

#status bar(song length)
status_bar = Label(root,text='',bd=1,relief='flat',anchor='center',bg="#a5d673")
status_bar.pack(fill="x",side="bottom",ipady=2)


my_slider = ttk.Scale(main_frame,from_=0,to=100,orient='horizontal',value=0,command=slide,length=360)
my_slider.grid(row=2,column=0,pady=10)

vol_slider = ttk.Scale(vol_frame,from_=1,to=0,orient='vertical',value=1,command=volume,length=120)
vol_slider.pack(pady=5)

root.mainloop()

import os

# Check if the "install_dependencies.py" script exists
if os.path.exists("install_dependencies.py"):
    # Execute the script to install dependencies
    os.system("python install_dependencies.py")


import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube, Playlist, Channel
from pytube.exceptions import VideoUnavailable

# Function to browse and select a directory
def select_directory():
    directory = filedialog.askdirectory()
    directory_var.set(directory)

# Function to download a single video
def download_single_video():
    url = single_video_var.get()
    directory = directory_var.get()

    def update_progress_bar(stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = (bytes_downloaded / file_size) * 100
        download_progress_var.set(progress)
    
    try:
        yt = YouTube(url, on_progress_callback=update_progress_bar)
        messagebox.showinfo("Info", f'{yt.title} Video Downloading...')
        yt.streams.get_highest_resolution().download(directory)
        download_progress_var.set(100)  # Set progress to 100% when download is complete
        messagebox.showinfo("Info", 'Video Downloaded...')
    except (VideoUnavailable, Exception):
        messagebox.showerror("Error", 'Video is not accessible')

# Function to download from a playlist
def download_playlist():
    playlist_url = playlist_var.get()
    directory = directory_var.get()
    
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.video_urls)
    
    pMenu = playlist_menu_var.get()
    
    if pMenu == 1:
        for video in playlist.videos:
            try:
                video.register_on_progress_callback(on_progress)
                messagebox.showinfo("Info", f'{video.title} Video Downloading...')
                video.streams.get_highest_resolution().download(directory)
                messagebox.showinfo("Info", f'{video.title} Video Downloaded')
            except VideoUnavailable:
                messagebox.showerror("Error", f'{video.title} is unavailable, skipping.')
    elif pMenu == 2:
        nChoice = int(recent_choice_var.get())
        for video in playlist.videos[:nChoice]:
            try:
                video.register_on_progress_callback(on_progress)
                messagebox.showinfo("Info", f'{video.title} Video Downloading...')
                video.streams.get_highest_resolution().download(directory)
                messagebox.showinfo("Info", f'{video.title} Video Downloaded')
            except VideoUnavailable:
                messagebox.showerror("Error", f'{video.title} is unavailable, skipping.')

# Function to download from a channel
def download_channel():
    channel_link = channel_var.get()
    directory = directory_var.get()
    
    channel = Channel(channel_link)
    total_videos = len(channel.video_urls)
    
    choise = channel_menu_var.get()
    
    if choise == 1:
        for video in channel.videos:
            try:
                video.register_on_progress_callback(on_progress)
                messagebox.showinfo("Info", f'{video.title} Video Downloading...')
                video.streams.get_highest_resolution().download(directory)
                messagebox.showinfo("Info", f'{video.title} Video Downloaded')
            except VideoUnavailable:
                messagebox.showerror("Error", f'{video.title} is unavailable, skipping.')
    elif choise == 2:
        recentChoice = int(channel_recent_choice_var.get())
        for video in channel.videos[:recentChoice]:
            try:
                video.register_on_progress_callback(on_progress)
                messagebox.showinfo("Info", f'{video.title} Video Downloading...')
                video.streams.get_highest_resolution().download(directory)
                messagebox.showinfo("Info", f'{video.title} Video Downloaded')
            except VideoUnavailable:
                messagebox.showerror("Error", f'{video.title} is unavailable, skipping.')

# Function to update the progress bar
def on_progress(stream, chunk, bytes_remaining):
    file_size = stream.filesize
    bytes_downloaded = file_size - bytes_remaining
    progress = (bytes_downloaded / file_size) * 100
    download_progress_var.set(progress)

# Create the main window
root = tk.Tk()
root.title("YouTube Downloader")

# Create and set a StringVar to store the download directory
directory_var = tk.StringVar()
directory_var.set("DOWNLOAD FOLDER")

# Create a label to display the selected download directory
directory_label = ttk.Label(root, text="Download Directory:")
directory_label.grid(row=0, column=0)

# Create an entry field to display the selected directory
directory_entry = ttk.Entry(root, textvariable=directory_var)
directory_entry.grid(row=0, column=1)

# Create a Browse button to select the download directory
browse_button = ttk.Button(root, text="Browse", command=select_directory)
browse_button.grid(row=0, column=2)

# Create a notebook for tabbed interface
notebook = ttk.Notebook(root)
notebook.grid(row=1, column=0, columnspan=3)

# Create tabs for single video, playlist, and channel
single_video_tab = ttk.Frame(notebook)
playlist_tab = ttk.Frame(notebook)
channel_tab = ttk.Frame(notebook)

notebook.add(single_video_tab, text="Single Video")
notebook.add(playlist_tab, text="Playlist")
notebook.add(channel_tab, text="Channel")

# ----------------------------------------
# Single Video Tab
# ----------------------------------------

# Create and set a StringVar to store the single video URL
single_video_var = tk.StringVar()

# Create a label for single video URL
single_video_label = ttk.Label(single_video_tab, text="Video URL:")
single_video_label.grid(row=0, column=0)

# Create an entry field for the single video URL
single_video_entry = ttk.Entry(single_video_tab, textvariable=single_video_var, width=50)
single_video_entry.grid(row=0, column=1)

# Create a button to download a single video
single_video_button = ttk.Button(single_video_tab, text="Download", command=download_single_video)
single_video_button.grid(row=0, column=2)

# Create a progress bar for single video download
download_progress_var = tk.DoubleVar()
download_progress_var.set(0)

download_progress_bar = ttk.Progressbar(single_video_tab, variable=download_progress_var, length=30)
download_progress_bar.grid(row=0, column=3)

# ----------------------------------------
# Playlist Tab
# ----------------------------------------

# Create and set a StringVar to store the playlist URL
playlist_var = tk.StringVar()

# Create a label for the playlist URL
playlist_label = ttk.Label(playlist_tab, text="Playlist URL:")
playlist_label.grid(row=0, column=0)

# Create an entry field for the playlist URL
playlist_entry = ttk.Entry(playlist_tab, textvariable=playlist_var, width=50)
playlist_entry.grid(row=0, column=1)

# Create a label for the playlist menu
playlist_menu_label = ttk.Label(playlist_tab, text="Select an option:")
playlist_menu_label.grid(row=1, column=0)

# Create a menu for selecting options (all videos or recent)
playlist_menu_var = tk.IntVar()
playlist_menu = ttk.Combobox(playlist_tab, textvariable=playlist_menu_var, values=["Download all videos", "Download recent videos"])
playlist_menu.grid(row=1, column=1)
playlist_menu.set("Download all videos")

# Create an entry field for selecting the number of recent videos
recent_choice_label = ttk.Label(playlist_tab, text="Number of recent videos:")
recent_choice_label.grid(row=2, column=0)

recent_choice_var = tk.StringVar()
recent_choice_entry = ttk.Entry(playlist_tab, textvariable=recent_choice_var)
recent_choice_entry.grid(row=2, column=1)

# Create a button to download from a playlist
playlist_button = ttk.Button(playlist_tab, text="Download", command=download_playlist)
playlist_button.grid(row=3, column=0, columnspan=2)

# ----------------------------------------
# Channel Tab
# ----------------------------------------

# Create and set a StringVar to store the channel URL
channel_var = tk.StringVar()

# Create a label for the channel URL
channel_label = ttk.Label(channel_tab, text="Channel URL:")
channel_label.grid(row=0, column=0)

# Create an entry field for the channel URL
channel_entry = ttk.Entry(channel_tab, textvariable=channel_var, width=50)
channel_entry.grid(row=0, column=1)

# Create a label for the channel menu
channel_menu_label = ttk.Label(channel_tab, text="Select an option:")
channel_menu_label.grid(row=1, column=0)

# Create a menu for selecting options (all videos or recent)
channel_menu_var = tk.IntVar()
channel_menu = ttk.Combobox(channel_tab, textvariable=channel_menu_var, values=["Download all videos", "Download recent videos"])
channel_menu.grid(row=1, column=1)
channel_menu.set("Download all videos")

# Create an entry field for selecting the number of recent videos
channel_recent_choice_label = ttk.Label(channel_tab, text="Number of recent videos:")
channel_recent_choice_label.grid(row=2, column=0)

channel_recent_choice_var = tk.StringVar()
channel_recent_choice_entry = ttk.Entry(channel_tab, textvariable=channel_recent_choice_var)
channel_recent_choice_entry.grid(row=2, column=1)

# Create a button to download from a channel
channel_button = ttk.Button(channel_tab, text="Download", command=download_channel)
channel_button.grid(row=3, column=0, columnspan=2)

root.mainloop()

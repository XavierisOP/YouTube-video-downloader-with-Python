import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pytube import YouTube, Playlist, Channel
from pytube.exceptions import VideoUnavailable, RegexMatchError
import threading

# Create a shared variable to control download threads
stop_download = False
download_thread = None

# Function to browse and select a directory
def select_directory():
    directory = filedialog.askdirectory()
    directory_var.set(directory)

# Function to download a single video
def download_single_video():
    global download_thread, stop_download
    if download_thread and download_thread.is_alive():
        messagebox.showinfo("Info", "Download is already in progress.")
        return

    url = single_video_var.get()
    directory = directory_var.get()

    def update_progress_bar(stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = (bytes_downloaded / file_size) * 100
        download_progress_var.set(progress)

    def download_single_video_thread():
        try:
            yt = YouTube(url, on_progress_callback=update_progress_bar)
            messagebox.showinfo("Info", f'{yt.title} Video Downloading...')
            yt.streams.get_highest_resolution().download(directory)
            download_progress_var.set(0)  # Reset progress bar
            messagebox.showinfo("Info", 'Video Downloaded...')
        except (VideoUnavailable, Exception):
            messagebox.showerror("Error", 'Video is not accessible')

    # Reset the stop_download variable
    stop_download = False

    # Run the download in a separate thread
    download_thread = threading.Thread(target=download_single_video_thread)
    download_thread.start()

# Function to download from a playlist
def download_playlist():
    global download_thread, stop_download
    if download_thread and download_thread.is_alive():
        messagebox.showinfo("Info", "Download is already in progress.")
        return

    playlist_url = playlist_var.get()
    directory = directory_var.get()

    def update_progress_bar(stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = (bytes_downloaded / file_size) * 100
        playlist_progress_var.set(progress)

    def download_playlist_thread():
        playlist = Playlist(playlist_url)
        total_videos = len(playlist.video_urls)
        for i, video in enumerate(playlist.videos, start=1):
            if stop_download:
                break

            try:
                video.register_on_progress_callback(update_progress_bar)
                messagebox.showinfo("Info", f'Downloading Video {i}/{total_videos}: {video.title}')
                video.streams.get_highest_resolution().download(directory)
                playlist_progress_var.set((i / total_videos) * 100)
                messagebox.showinfo("Info", f'Video {video.title} Downloaded')
            except VideoUnavailable:
                messagebox.showerror("Error", f'Video {video.title} is unavailable.')

    # Reset the stop_download variable
    stop_download = False

    # Run the download in a separate thread
    download_thread = threading.Thread(target=download_playlist_thread)
    download_thread.start()

# Function to download from a channel
def download_channel():
    global download_thread, stop_download
    if download_thread and download_thread.is_alive():
        messagebox.showinfo("Info", "Download is already in progress.")
        return

    channel_link = channel_var.get()
    directory = directory_var.get()

    def update_progress_bar(stream, chunk, bytes_remaining):
        file_size = stream.filesize
        bytes_downloaded = file_size - bytes_remaining
        progress = (bytes_downloaded / file_size) * 100
        channel_progress_var.set(progress)

    def download_channel_thread():
        try:
            channel = Channel(channel_link)
            total_videos = len(channel.video_urls)
            for i, video in enumerate(channel.videos, start=1):
                if stop_download:
                    break

                try:
                    video.register_on_progress_callback(update_progress_bar)
                    messagebox.showinfo("Info", f'Downloading Video {i}/{total_videos}: {video.title}')
                    video.streams.get_highest_resolution().download(directory)
                    channel_progress_var.set((i / total_videos) * 100)
                    messagebox.showinfo("Info", f'Video {video.title} Downloaded')
                except VideoUnavailable:
                    messagebox.showerror("Error", f'Video {video.title} is unavailable.')
        except RegexMatchError:
            messagebox.showerror("Error", 'Invalid Channel URL.')

    # Reset the stop_download variable
    stop_download = False

    # Run the download in a separate thread
    download_thread = threading.Thread(target=download_channel_thread)
    download_thread.start()

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

# Create a progress bar for Single Video Tab
download_progress_var = tk.DoubleVar()
download_progress_var.set(0)

single_video_progress_bar = ttk.Progressbar(single_video_tab, variable=download_progress_var, length=100)
single_video_progress_bar.grid(row=1, column=0, columnspan=3)

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

# Create a button to download from a playlist
playlist_button = ttk.Button(playlist_tab, text="Download", command=download_playlist)
playlist_button.grid(row=1, column=0, columnspan=2)

# Create a progress bar for Playlist Tab
playlist_progress_var = tk.DoubleVar()
playlist_progress_var.set(0)

playlist_progress_bar = ttk.Progressbar(playlist_tab, variable=playlist_progress_var, length=100)
playlist_progress_bar.grid(row=2, column=0, columnspan=2)

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

# Create a button to download from a channel
channel_button = ttk.Button(channel_tab, text="Download", command=download_channel)
channel_button.grid(row=1, column=0, columnspan=2)

# Create a progress bar for Channel Tab
channel_progress_var = tk.DoubleVar()
channel_progress_var.set(0)

channel_progress_bar = ttk.Progressbar(channel_tab, variable=channel_progress_var, length=100)
channel_progress_bar.grid(row=2, column=0, columnspan=2)

# Create a label for "Xavier" at the bottom right
xavier_label = ttk.Label(root, text="In Channel will update soon.. - Xavier  ")
xavier_label.grid(row=4, column=2, sticky="se")  # Use the sticky option to place it at the bottom right

root.mainloop()

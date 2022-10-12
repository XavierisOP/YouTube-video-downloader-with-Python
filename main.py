import pytube
from pytube import YouTube, Playlist, Channel, exceptions
from pytube.cli import on_progress

fuchsia = '\033[38;2;255;00;255m'
# color as hex #FF00FF
reset_color = '\033[39m'

def progress(streams, chunk: bytes, bytes_remaining: int):
    contentsize = video.filesize
    size = contentsize - bytes_remaining

    print('\r' + '[Download progress]:[%s%s]%.2f%%;' % (
    '█' * int(size*20/contentsize), ' '*(20-int(size*20/contentsize)), float(size/contentsize*100)), end='')
print("""
██╗  ██╗█████╗ ██╗   ██╗██╗███████╗██████╗ 
╚██╗██╔╝██╔══██╗██║   ██║██║██╔════╝██╔══██╗
 ╚███╔╝ ███████║██║   ██║██║█████╗  ██████╔╝
 ██╔██╗ ██╔══██║╚██╗ ██╔╝██║██╔══╝  ██╔══██╗
██╔╝ ██╗██║  ██║ ╚████╔╝ ██║███████╗██║  ██║
╚═╝  ╚═╝╚═╝  ╚═╝  ╚═══╝  ╚═╝╚══════╝╚═╝  ╚═╝
""")
while True:
    directory = input("Enter a Directiory where all video will be download! » ")
    menu = int(input("""
CHOOSE THE OPTION ACCORDING TO YOUR NEED - 
[01] » Downlaod a Single Video
[02] » Download From PlayList
[03] » Download From a Channel
[INPUT] Enter your choice! » """))

    # SINGLE VIDEO DOWNLOAD
    if menu == 1:
        url = (input("""
Download for a Single Video - 
[INPUT] Enter a video URL! » """))
        try:
            yt = YouTube(url,on_progress_callback=on_progress)
            print(f'{yt.title} Video Downloading...')
            yt.streams.get_highest_resolution().download(directory)
            print('Video Downloaded...')
        except exceptions.VideoPrivate:
            print('Video is Private') 
        except exceptions.VideoRegionBlocked:
            print('Video is blocked')
            
        except exceptions.VideoUnavailable:
            print('Video is Unavailable')


    # PLAYLIST DOWNLOAD FULL & Recent
    elif menu == 2:
        playlist_url = (input("""
Download From a PlayList - 
[INPUT] Enter a Playlist URL! » """))
        playlist = Playlist(playlist_url)
        print("Total Videos", len(playlist.video_urls))

        pMenu = int(input("""
Download PlayList Bulk or Selective - 
[01] » Downlaod all Videos From Playlist
[02] » Downlaod Recently Uploaded Videos From Playlist
[INPUT] Enter your choice! » """))
        
        
        if pMenu  == 1:
            
            for video in playlist.videos:
                try:
                    video.register_on_progress_callback(on_progress)
                    print(f'{video.title} is Downlaoding.')
                    video.streams.get_highest_resolution().download(directory)
                    print(f'{video.title} is Downloaded')
                except VideoUnavailable:
                    print(f'{video.title} is unavaialable, skipping.')
        elif pMenu  == 2:
            nChoise = int(input("""
Download Recent Video From PlayList -
[INPUT] Enter No. of Recent Videos You want to Download..! » """))

            for video in playlist.videos[:nChoise]:
                try:
                    video.register_on_progress_callback(on_progress)
                    print(f'{video.title} is Downlaoding.')
                    video.streams.get_highest_resolution().download(directory)
                    print(f'{video.title} is Downloaded')
                except VideoUnavailable:
                    print(f'{video.title} is unavaialable, skipping.')
        else:
            print(f'INVALID INPUT') 
            pass     



    elif menu == 3:
        channel_link = (input("""
Download From a Channel - 
[INPUT] Enter a Channel URL! » """))
        channel = Channel(channel_link)
        print(channel.channel_name)
        print(channel.channel_url)
        print("Total Videos", len(channel.video_urls))
        choise = int(input("""
Download From Channel Bulk or Selective - 
[01] » Downlaod all Videos From Channel
[02] » Downlaod Recently Uploaded Videos From Channel
[INPUT] Enter your choice! » """))
        if choise == 1:
            
            for video in channel.videos:
                try:
                    print(f'{video.title} is Downlaoding.')
                    video.register_on_progress_callback(on_progress)
                    video.streams.get_highest_resolution().download(directory)
                except VideoUnavailable:
                    print(f'{video.title} is unavaialable, skipping.')
        elif choise == 2:
            recentChoise = int(input("""
Download Recent Video From Channel -
[INPUT] Enter No. of Recent Videos You want to Download..! » """))

            for video in channel.videos[:recentChoise]:
                try:
                    print(f'{video.title} is Downlaoding.')
                    video.register_on_progress_callback(on_progress)
                    video.streams.get_highest_resolution().download(directory)
                    print(f'{video.title} is Downloaded')
                except VideoUnavailable:
                    print(f'{video.title} is unavaialable, skipping.')
        else:
            print(f'INVALID INPUT')   
            pass         

    else:
        print(f'INVALID INPUT') 
        pass

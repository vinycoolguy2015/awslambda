from __future__ import unicode_literals
from Tkinter import *
import youtube_dl
import tkMessageBox



def downlaod(url):
    ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    }
    try:
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        tkMessageBox.showinfo("Youtube downloader", "Download completed")
    except :
        tkMessageBox.showinfo("Youtube downloader","Can't download the requested url. Make sure you have internet working and provided a valid URL")
    
        

    
    
master = Tk()
master.configure(background='brown')
master.geometry("250x70")
Label(master, text="Youtube URL").grid(row=0)

e1 = Entry(master)
e1.grid(row=0, column=1,padx=(10, 10))

Button(master, text='Download',command=lambda: downlaod(e1.get())).grid(row=2, column=0, sticky=W, pady=4)
Button(master, text='Exit', command=master.quit).grid(row=2, column=1, sticky=W, pady=4)

mainloop()

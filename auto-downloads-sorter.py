import os
from os.path import splitext, exists
import shutil
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


source_dir = "~/Downloads"
dest_dir_music = "~/Desktop/Downloads/Music"
dest_dir_vid = "~/Desktop/Downloads/Videos"
dest_dir_img = "~/Desktop/Downloads/Images"
dest_dir_pkg = "~/Desktop/Downloads/Packages"

def makeUnique(path):
    filename, extension = splitext(path)
    counter = 1
    while exists(path):
        path = f"{filename} ({counter}){extension}"
        counter += 1

    return path
    
    
def move(dest, entry, name):
    file_exists = os.path.exists(dest + "/" + name)
    if file_exists:
        unique_name = makeUnique(name)
        os.rename(entry, unique_name)
    shutil.move(entry, dest)
    
class MoverHandler(FileSystemEventHandler):
    def on_modified(self, event):
        with os.scandir(source_dir) as entries:
            for entry in entries:
                name = entry.name
                dest = source_dir
                if name.endswith('.wav') or name.endswith('.mp3') or name.endswith('.m4a'):
                    dest = dest_dir_music
                    move(dest, entry, name)
                    
                elif name.endswith('.mov') or name.endswith('.mp4'):
                    dest = dest_dir_vid
                    move(dest, entry, name)
                elif name.endswith('.jpg') or name.endswith('.jpeg') or name.endswith('.png'):
                    dest = dest_dir_img
                    move(dest, entry, name)
                elif name.endswith('.gz'):
                    dest = dest_dir_pkg
                    move(dest, entry, name)
    
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = source_dir
    event_handeler = MoverHandler()
    observer = Observer()
    observer.schedule(event_handeler, path, recursive = True)
    observer.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()



import numpy as np
import os
import time
from tqdm.notebook import tqdm
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileCreatedEvent

timestr = time.strftime("%Y.%m.%d-%H.%M.%S")

class DirectoryWatcher:

    def __init__(self, directory_to_watch, watch_time_interval=0.5):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch
        self.watch_time_interval = watch_time_interval

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(self.watch_time_interval)
                
        except:
            self.observer.stop()
            print("Error")

        self.observer.join()


class Handler(FileSystemEventHandler):
    
    def __init__(self):
        self.path_strings = []

    def on_created(self, event):

        if isinstance(event, FileCreatedEvent):
            
            self.path_strings.append(event.src_path)
            self.path_strings = self.path_strings[-number_of_curves:]


# w = DirectoryWatcher(data_directory, watch_time_interval=0.5)
# w.run()


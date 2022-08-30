import os
import time
import tqdm
from itertools import cycle, takewhile, dropwhile


class CyclicalList:
    """
    Cyclical list
    refer to https://stackoverflow.com/a/65133964
    """
    def __init__(self, initial_list):
        self._initial_list = initial_list

    def __getitem__(self, item):
        if isinstance(item, slice):
            if item.stop is None:
                raise ValueError("Cannot slice without stop")
            iterable = enumerate(cycle(self._initial_list))
            if item.start:
                iterable = dropwhile(lambda x: x[0] < item.start, iterable)
            return [
                element
                for _, element in takewhile(lambda x: x[0] < item.stop, iterable)
            ]

        for index, element in enumerate(cycle(self._initial_list)):
            if index == item:
                return element

    def __iter__(self):
        return cycle(self._initial_list)

class DirectoryReplay:
    def __init__(self, experiment_directory, range=(0,9999)):
        """ 
        Replay an experiment from a given directory
        """
        self.experiment_directory = experiment_directory
        self.range = range
        self.counter = self.range[0]
        self.files = sorted(os.listdir(self.experiment_directory))[self.range[0] : self.range[1]]
        self.files_loop = CyclicalList(self.files)
        self.files_len = len(self.files)
    
    def fetchData(self, instantly=True, time_interval=0.5, number_of_curves=10):
        while self.counter <= self.range[1]:
            batch = []
            for file in self.files[self.counter:number_of_curves + self.counter]:
                if not instantly:
                    time.sleep(time_interval) # wait for given time interval
                batch.append(os.path.join(self.experiment_directory, file))
            self.counter += 1
            yield batch
    
    def fetchDataLoop(self, instantly=True, time_interval=0.5, number_of_curves=10):
        while True:
            batch = []
            for file in self.files_loop[self.counter:number_of_curves + self.counter]:
                if not instantly:
                    time.sleep(time_interval) # wait for given time interval
                batch.append(os.path.join(self.experiment_directory, file))
            self.counter += 1
            yield batch
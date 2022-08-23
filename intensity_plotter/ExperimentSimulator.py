
import os
import time
import numpy as np
import tqdm

class ExperimentSimulator(object):
    
    def __init__(self, source,target, time_interval=0.1, noise_coefficient=10):
        """ 
        Simulate moving files one by one from source directory to target in random time intervals.
        time interval is 0.1 sec by default
        noise_coefficient is 10 by default (which means it is 10 times lower than the actual value).
        """
        self.source = source
        self.target = target
        self.time_interval = time_interval
        self.noise_coefficient = noise_coefficient
    
    def runForward(self, instantly=False, reverse_order=False):
        
        for file in tqdm(sorted(os.listdir(self.source), reverse=reverse_order)):
            if not instantly:
                time.sleep(self.time_interval + np.random.rand() * (self.time_interval / self.noise_coefficient)) # wait for random time interval
            os.rename(os.path.join(self.source, file), os.path.join(self.target, file)) # move to target
    
    
    def runReverse(self, instantly=False, reverse_order=False):
        for file in tqdm(sorted(os.listdir(self.source), reverse=reverse_order)):
            if not instantly:
                time.sleep(self.time_interval + np.random.rand() * (self.time_interval / self.noise_coefficient)) # wait for random time interval
            os.rename(os.path.join(self.target, file), os.path.join(self.source, file)) #move to source
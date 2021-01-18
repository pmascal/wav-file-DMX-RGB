"""
@author: pmascal
"""

import numpy as np
from scipy import signal
from scipy.io import wavfile

class DMXMusic:
    
    def __init__(self, wavfilename, user_ch = False, user_rgb = False):
        """
        creates DMXMusic object
            ----------
            Parameters
            ----------
            wavfilename = name of the .wav file to be processed
            brightness,red,green,blue_ch = DMX channel designated, not 0 indexed (optional)
            red,green,blue_min,max = the ranges of RGB frequencies (optional)
            red is lowest, then green, then blue.
        """
        
        if not user_ch:
            self.brightness_ch = 1
            self.red_ch = 2
            self.green_ch = 3
            self.blue_ch = 4
        else:
            self.brightness_ch = input("Brightness Channel: ")
            self.red_ch = input("Red Channel: ")
            self.green_ch = input("Green Channel: ")
            self.blue_ch = input("Blue Channel: ")
        
        # self.user_rgb = user_rgb
        if user_rgb:
            self.red_max = input("Max Frequency for Red: ")
            self.green_min = input("Min Freqency for Green: ")
            self.green_max = input("Max Frequency for Green: ")
            self.blue_min = input("Min Frequency for Blue")
        
        # Call the functions to create all the data
        self.Spectrogram(wavfilename)
        self.AverageValues()
        self.FrameData(user_rgb)
        
        
#############################################################################
    

    def Spectrogram(self, wavfilename):
        """
        Collects frequency, time, and amplitude information
        """
        
        sample_rate, samples = wavfile.read(wavfilename)
        self.frequencies, self.times, self.spectrogram = signal.spectrogram(samples, fs = sample_rate)
    
    
#############################################################################


    def AverageValues(self):
        """
        Calculate the overall average frequency/amplitude for each frame
        """
        
        self.avg_vals = []
        self.amp_vals = []
        
        for amplitudes in self.spectrogram.T:
            
            if sum(amplitudes) == 0:
                self.avg_vals.append(0)
            else:
                self.avg_vals.append(np.average(self.frequencies, weights=amplitudes))
                
            self.amp_vals.append(np.average(amplitudes))
        
#############################################################################


    def FrameData(self,user_rgb):
        """
        Scale each value and assign to their frame.
        """
        
        # Initialize a dictionary that will have keys be the times that define
        # each frame, and values be brightness, red, green, and blue values.
        self.frame_data = {}
        
        # Set the scaled range to be from 0 to 255.
        a = 0
        b = 255
        
        # Calculate the min and max of the audio's frequencies and amplitudes.
        avgfreq_min, avgfreq_max = int(min(self.avg_vals)), int(max(self.avg_vals))
        ampfreq_min, ampfreq_max = int(min(self.amp_vals)), int(max(self.amp_vals))
       
        # A user is capable of giving the frequency bin parameters initially,
        # but if none were given, calculate based on range of frequencies.
        if not user_rgb:
            self.red_max = int(avgfreq_max/2)
            self.green_min = int(self.red_max/2)
            self.blue_min = int(self.red_max)
            self.green_max = int(0.5*(avgfreq_max-self.blue_min)+self.red_max)
        
        
        # Give each frame RGB and brightness values
        for i in range(len(self.avg_vals)):
            
            # Assign they key (time) to a list of 4 0's
            self.frame_data[self.times[i]] = [0]*4
            
            # Adds the brightness level, depends on average amplitude
            self.frame_data[self.times[i]][self.brightness_ch-1] = [(b-a)*(self.amp_vals[i]-ampfreq_min)/(ampfreq_max - ampfreq_min)+a]+[0]*3
            
            # Scale each color's value based on frequency bin parameters as 
            # well as overall min/max of audio file.
            red_val = (b-a)*(self.avg_vals[i]-avgfreq_min)/(self.red_max - avgfreq_min)+a
            green_val = (b-a)*(self.avg_vals[i]-self.green_min)/(self.green_max - self.green_min)+a
            blue_val = (b-a)*(self.avg_vals[i]-self.blue_min)/(avgfreq_max - self.blue_min)+a
            
            
            # If the frequency is below/above the color's min/max boundary,
            # its value will be below 0 or above 255, respectively.
            if red_val > 0 and red_val < 255:
                self.frame_data[self.times[i]][self.red_ch - 1] = red_val
            if green_val > 0 and green_val < 255:
                self.frame_data[self.times[i]][self.green_ch-1] = green_val
            if blue_val > 0 and blue_val < 255:
                self.frame_data[self.times[i]][self.blue_ch-1] = blue_val
            
#############################################################################
    
    def tcolor(self, t):
        """
        Returns a single frame's data relevant to any time given.
        """
        
        if t < 0 or t > self.times[-1]:
            raise Exception('Time given was outside audio sample')
        elif t<self.times[0]:
            return np.array(self.frame_data[self.times[0]]+[0]*508)
        else:
            return np.array(self.frame_data[self.times[self.times <= t][-1]]+[0]*508)
        
#############################################################################
#############################################################################
#############################################################################

# Asks the user what .wav file they would like to process
def userinput():
    wavfilename = input('Name of .wav file: ')
    if wavfilename[-4:] != '.wav':
        wavfilename += '.wav'
    return wavfilename

# Plot frequency, brightness, red, green, and blue all versus time for
# visualization
def plot():
    import matplotlib.pyplot as plt
    
    avgfreq_min, avgfreq_max = int(min(DMX.avg_vals)), int(max(DMX.avg_vals))
    scaled_avg = []
    for freq in DMX.avg_vals:
        scaled_avg.append((255-0)*(freq-avgfreq_min)/(avgfreq_max - avgfreq_min)+0)
    
    scaled_amp = []
    red = []
    green = []
    blue = []
    
    for i in times:
        scaled_amp.append(DMX.tcolor(i)[0])
        red.append(DMX.tcolor(i)[1])
        green.append(DMX.tcolor(i)[2])
        blue.append(DMX.tcolor(i)[3])
    
    plt.plot(times, scaled_avg,'k', times, scaled_amp,'y', times, red,'r', times, green,'g', times, blue,'b')
    plt.legend(['Frequency', 'Brightness'], loc=0)
    plt.xlabel('seconds')
    plt.ylabel('0-255 scale')
    plt.show()

def time(wavfilename):
    from timeit import default_timer as timer
    import statistics
    
    start = timer()
    DMX=DMXMusic(wavfilename)
    end = timer()
    print("Initialization: ",end - start)
    
    t = []
    for i in range(int(DMX.times[-1]-1)):
        start = timer()
        DMX.tcolor(i)
        end = timer()
        t.append(end-start)
    print("Call for time: ", statistics.mean(t))

#############################################################################
#############################################################################
#############################################################################

if __name__ == "__main__":
    
    wavfilename = 'increasing.wav'
    # wavfilename = userinput()
    
    # time(wavfilename)
    
    DMX = DMXMusic(wavfilename)
    
    spectrogram = DMX.spectrogram
    frequencies = DMX.frequencies
    times = DMX.times
    average_values = DMX.avg_vals
    amplitude_values = DMX.amp_vals
    FrameData = DMX.frame_data
    
    plot()
    
    # DMX_signal = DMX.tcolor(t)

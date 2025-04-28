import cv2 as cv
import lfdfiles as lfd
import numpy as np
import statistics as stat
import tkinter as tk

from matplotlib import pyplot as plt
from tkinter import filedialog

#layout: for each image selected, create named images (what they simply look like), organize in a bar plot, and plot the phase 
# with the color indicating intensity

#simply adds phase and mod value of pixel to a list for the phase plot
def add_phase(phase, added_phase, mod, added_mod, intensity, added_intensity):
    for y in range(added_phase.shape[0]):
        for x in range(added_phase.shape[1]):
            phase.append(added_phase[x, y] * np.pi /180)
            mod.append(added_mod[x, y])
            intensity.append(added_intensity[x, y])
    return phase, mod, intensity

#removes data for all lists if it is below the 1st quartile in intensity
def quartile(phase, mod, intensity):
    sorted_intensity = [*set(intensity)]
    sorted_intensity.sort()
    if (len(sorted_intensity) % 2 != 0):
        median_index = int((len(sorted_intensity) + 1) / 2)
    else:
        median_index = int(len(sorted_intensity) / 2)
    quartile_index = median_index - int((median_index) / 2)
    quartile = sorted_intensity[quartile_index]
    for i in range(len(intensity)):
        if intensity[i] < quartile:
            phase[i], mod[i], intensity[i] = 0, 0, 0
    return phase, mod, intensity

def phase_plot(phase, mod, intensity):
    #graphing stuff
    max_phase = round(max(phase), 1)
    nonzero_indices = np.nonzero(phase)
    nonzero_phases = []
    for i in nonzero_indices[0]:
        nonzero_phases.append(phase[i])
    min_phase = round(min(nonzero_phases), 1)
    fig = plt.figure()
    ax = fig.add_subplot(projection = 'polar')
    ax.set_yticklabels([])
    ax.set_xticks(np.arange((min_phase - .1), (max_phase + .1), .1))
    ax.set_thetamin((min_phase - .1) * 180 / np.pi)
    ax.set_thetamax((max_phase + .1) * 180 / np.pi)
    angle_pos = ax.get_xticks()
    angle_pos = [round(label, 3) for label in angle_pos]
    ax.set_xticklabels(angle_pos)
    colors = intensity
    theta = phase
    r = mod
    ax.scatter(theta, r, c = colors, s = .15, linewidths = 0, cmap = 'jet', marker = ',')
    plt.show()
    
def main():
    #initialize any variables, like lists for the graphs
    #*intensity is also added to handle quartile/median type data
    intensity = []
    phase = []
    mod = []
    
    #file dialogue
    root = tk.Tk()
    root.withdraw()
    filePaths = filedialog.askopenfilenames()
    
    for fileName in filePaths:
        #opens images, uses cv2 blur, adds the data to the relevant list
        img = lfd.SimfcsR64(fileName).asarray()
        intensity_array = img[0,:,:]
        intensity_array = cv.blur(intensity_array, (3, 3))
        phase_array = img[1,:,:]
        phase_array = cv.blur(phase_array, (3, 3))
        mod_array = img[2,:,:]
        mod_array = cv.blur(mod_array, (3,3))
        phase, mod, intensity = add_phase(phase, phase_array, mod, mod_array, intensity, intensity_array)
        
    phase, mod, intensity = quartile(phase, mod, intensity)
    phase_plot(phase, mod, intensity)
    
if __name__ == "__main__":
    main()
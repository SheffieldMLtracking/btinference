from alignment import Camera
import json
from pathlib import Path
import numpy as np
import re
from pathinference.helper import confidence_ellipse

def getcamsetid(path):
    """
    Convert a path to a id string for a unique box/camera.
    """
    return '/'.join(path.parts[-2:])

def getcameras(calsetpaths,alignmentsourcename):
    """
    Given a list of calibration set paths, return a dictionary of cameras; indexed by a string of 'box/cam'.
    calsetpaths : A list of pathlib paths to the calibration sets
    alignmentsourcename : the name of the calibration source (e.g. btalignment)
    """
    #create the camera objects from the alignment data...
    cameras = {}
    for path in calsetpaths:
        #print("Looking in %s for camera" % path)
        jsonfile = path.joinpath(alignmentsourcename+'/alignment.json')
        camsetid = getcamsetid(path)
        jsondata = json.load(open(jsonfile,'r'))
        cameras[camsetid] = Camera(loc=jsondata['loc'], orientation=jsondata['orientation'], hfov=jsondata['hfov'], vfov=jsondata['vfov'], res=jsondata['res'])
    return cameras
    
def totalsecsandms(st):
    time_hms = [int(s) for s in re.findall('([0-9]{1,2})[:\+]([0-9]{2})[:\+]([0-9]{2}).([0-9]{6})',st)[0]]
    return time_hms[0]*3600 + time_hms[1]*60 + time_hms[2]*1 + time_hms[3]/1e6
    
def getobservations(tagsetpaths,tagsource,cameras,after=0,before=np.inf):
    """
    Given a list of paths to the sets we want to use, the name of the tool that made the tags and the
    dictionary of cameras, return the list of observation times, and observations, and the filenames of where they were from.
    
    The observation times are an array of N times, the observations are a Nx6 array.
    
    tagsetpaths: list of paths to sets (e.g. ['Session1/set2/12/02G14695547',Session1/set2/14/02G06394393'])
    tagsource: name(s) of the source of the markers (e.g. btviewer), can be a string or list of strings.
    cameras: dictionary of cameras (indexed by 'box/cam')
    after: only include observations after this time (seconds since midnight)
    before: only include observations before this time (seconds since midnight)
    """
    
    if type(tagsource)==str: tagsource = [tagsource]
    obstimes = []
    observations = []
    obsfrom = []
    for path in tagsetpaths:
        warn_timestamp_once = False #we'll announce warnings and info on each of the folders...
        info_timestamp_once = False
        camsetid = getcamsetid(path)
        tagsourcefiles = []
        for source_string in tagsource:
            tagsourcefiles.extend(path.glob(source_string+'/*.json'))

        c = cameras[camsetid]
        for fn in tagsourcefiles:
            obstime = totalsecsandms(fn.as_posix())

            splits = fn.as_posix().split('/') #NEED TO USE Path stuff to do this cross-platform. sorry.
            timecorrection_fn = '/'.join(splits[:-2] + ['timecorrection'] + splits[-1:])
            try:
                timecorrection_jsondata = json.load(open(timecorrection_fn,'r'))   
                old_obstime = obstime
                obstime = totalsecsandms(timecorrection_jsondata['triggertimestring'])
                if not info_timestamp_once:
                    #print("------Applied Time Correction------")
                    #print("Loaded time correction data. Example from first record, for this camera:")
                    #print("Time Correction Filename: %s" % timecorrection_fn)
                    #print("New observation time: %0.5fs" % obstime)
                    #print("Old observation time: %0.5fs" % old_obstime)
                    #print("Difference: %0.5fs" % (obstime-old_obstime))
                    #print("Raw time correction data")
                    #print(timecorrection_jsondata)
                    #print("------------------------------------")
                    info_timestamp_once = True
            except:
                #we don't have a time correction file
                if not warn_timestamp_once: print("\n\n\n  Warning: Using filename as timestamp source\n\n\n")
                warn_timestamp_once = True
            if (obstime<after) or (obstime>before): continue #not in the requested time period
            jsondata = json.load(open(fn,'r'))
            if len(jsondata)==0: continue #this file doesn't have any observations in
            pixelcoord = np.array([jsondata[0]['x'],c.res[1]-jsondata[0]['y']]).astype(float)
            vect = c.get_pixel_local_vector(pixelcoord)
            
            obstimes.append(obstime)
            observations.append(np.r_[c.loc,vect])    
            obsfrom.append(fn)            
    observations = np.array(observations)
    obstimes = np.array(obstimes)
    return obstimes, observations, obsfrom
    
import matplotlib.pyplot as plt
import matplotlib.animation as animation
    
def makeanimation(times,observations,obstimes,M,C,animationfilename='animation.mp4'):
    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5,5)

    plt.axis('equal')
    plt.grid()
    #times = Xtest.numpy()[:int(len(Xtest.numpy())/3),0]
    mintime = np.min(times)
    maxtime = np.max(times)
    print(times.shape)
    print(M.shape)
    print("Making animation between times:")
    print(mintime,maxtime)
    def animate(i):
        ax.clear()
        for obs,t in zip(observations,obstimes):
            anitime = (i/10+mintime)
            alpha = 1-3*np.abs(t-anitime)
            
            if alpha>0:
                ax.plot([obs[0],obs[0]+obs[3]*10],[obs[1],obs[1]+obs[4]*10],color='grey',alpha=alpha)
                ax.add_patch(plt.Circle([obs[0],obs[1]],0.1,color='red'))
        

        ax.set_xlim([-1,10])
        ax.set_ylim([-5.5,5.5])
        
        idx = np.argmin(np.abs(times-(i/10+mintime)))
        pix = M[idx,:]
        ax.add_patch(confidence_ellipse(M[idx,0:2],C[idx,:2,:2],ax))

    ani = animation.FuncAnimation(fig, animate, frames=int(10*(maxtime-mintime)),
                        interval=100, repeat=False)
    plt.close()
    # Save the animation as an animated GIF
    #ani.save("simple_animation.gif", dpi=900, writer=PillowWriter(fps=0.1))
    FFwriter = animation.FFMpegWriter(fps=10)
    ani.save(animationfilename, writer = FFwriter) 

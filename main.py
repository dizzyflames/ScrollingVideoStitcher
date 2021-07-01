# Takes a video of a slow scrolling scenario and stitches the frames together into one long image
# I intend to use this for reading those mangas on youtube by stitching the scrolled video into one image

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os
import numpy as np
import cv2
from glob import glob
from PIL import Image
from natsort import natsorted


# downloads youtube video
def downloadVideo(url, name):
    file_loc = r"."
    print(file_loc)
    os.system("yt-dlp -o " + name + ".mp4 " + url)


# get frames at set interval of downloaded youtube video
def getFrames(filename, frameNum):
    cap = cv2.VideoCapture(filename)
    cap.set(1, frameNum)
    ret, frame = cap.read()
    cv2.imwrite(r"frames\frame" + str(frameNum) + ".png", frame)


# locates the images and stitches them all either horizontally or vertically
def stitchImages(frameArr):
    images = [Image.open(x) for x in
             frameArr]
    widths, heights = zip(*(i.size for i in images))

    total_height = sum(heights)
    max_width = max(widths)

    new_im = Image.new('RGB', (max_width, total_height))

    x_offset = 0
    y_offset = 0
    for im in images:
        new_im.paste(im, (x_offset, y_offset))
        y_offset += im.size[1]

    new_im.save('output.png')

# Downloads and stitches
def getImage():
    print("Enter youtube link: ")
    url = input()
    print("Enter video name: ")
    name = input()
    if url.lower() != "no":
        downloadVideo(url, name)

    filename = name + ".mp4"
    cap = cv2.VideoCapture(filename)
    numFrames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    print("\nThere are " + str(numFrames) + " frames")


    multiples = "factors of " + str(numFrames) + ": "
    for i in range(1,  numFrames + 1):
        if numFrames % i == 0:
            multiples += str(i) + " "

    print(multiples)
    print("138 worked pretty seamlessly for one of the videos I tried (depends on scroll speed)")

    print("\nEnter frame interval: ")
    interval = input()

    for x in range(numFrames):
        if not (x % int(interval)):
            getFrames(name + ".mp4", x)

    folder = r"C:\Users\jason\PycharmProjects\ScrollingVideoStitcher\frames"
    file_list = os.listdir(folder)
    file_list = natsorted(file_list)
    dir_list = [folder + "\\" + sub for sub in file_list]

    stitchImages(dir_list)

    print("Done")

getImage()


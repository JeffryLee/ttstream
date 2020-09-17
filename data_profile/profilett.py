import os
import subprocess
import re
from subprocess import Popen, PIPE
import matplotlib.pyplot as plt


def get_length(input_video):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)


def getWH(pathvideofile):
    in_pipe = Popen(["ffmpeg", "-i", "\"%s\"" % (pathvideofile)], stderr=PIPE)
    lines = in_pipe.stderr.readlines()
    w = 0
    h = 0
    for line in lines:
        rx = re.compile('.+Video.+, (\d{2,4})x(\d{2,4}).+')
        m = rx.match(str(line))
        if m is not None:
            w = int(m.group(1))
            h = int(m.group(2))
    return w, h


files = os.listdir("./video/")

lst = []
for file in files:
    filename = "./video/" + file
    w, h = getWH(filename)
    if w == 576 and h == 1024:
        lst.append((os.path.getmtime(filename), file))

lst.sort()

fd = open("log-tt.txt", "w")
dataratelst = []
for i in range(len(lst)):
    filename = "./video/" + lst[i][1]
    fsize = os.path.getsize(filename)
    fdura = get_length(filename)

    bitrate = fsize * 8 / 1000 / 1000 / fdura

    dataratelst.append(bitrate)
    fd.write("%s %f %f\n" % (filename, fdura, bitrate))

fd.close()


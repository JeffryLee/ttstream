import os
import subprocess



def get_length(input_video):
    result = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
         input_video], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return float(result.stdout)

files = os.listdir("./video_long/video/")

files.sort()


fd = open("log-long.txt", "w")
dataratelst = []

fdurapre = 0

for i in range(1, len(files)):
    filename = "./video_long/video/"+files[i]
    fsize = os.path.getsize(filename)
    fdura = get_length(filename)

    bitrate = fsize * 8 / 1000 / 1000 / (fdura - fdurapre)

    dataratelst.append(bitrate)
    fd.write("%s %f %f\n" % (filename, (fdura - fdurapre), bitrate))

    fdurapre = fdura

fd.close()


tmp  =1
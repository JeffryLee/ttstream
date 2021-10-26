import os

import requests
import numpy as np



def loadSwipe():
    filePath = "./dataclean/data/"
    filename = "173.72.39.74.txt"

    with open(filePath+filename, "r") as fd:
        lines = fd.readlines()
        print(lines)

    for i in range(len(lines)):
        lines[i] = lines[i].strip()

    dataret = []

    for i in range(len(lines)):
        dataret.append([])
        items = lines[i].split()

        dataret[i].append(items[0])
        dataret[i].append(items[1])
        dataret[i].append(int(items[2]))
        dataret[i].append(float(items[3]))
        dataret[i].append(float(items[4]))

    return dataret


def loadnetwork():
    nettrace = np.loadtxt("./networktrace/trace.txt")
    # print(np.shape(nettrace)[0])
    return nettrace

def loadchunktraces():
    pathprefix = "../contentServer/dash/data/"
    files = os.listdir(pathprefix)

    retdata = {}

    for file in files:
        fname = pathprefix + file

        nsegment = len(os.listdir(pathprefix+file)) // 6

        item = [0, []]

        item[0] = os.path.getsize(pathprefix + file + "/manifest.mpd")

        item[1].append([])
        for j in range(6):
            item[1][0].append(os.path.getsize(pathprefix + file + """/init-stream%d.m4s"""%(j)))

        for i in range(1, nsegment):
            item[1].append([])
            for j in range(5):
                item[1][i].append(os.path.getsize(pathprefix + file + """/chunk-stream%d-%05d.m4s"""%(j, i)))

        retdata[file] = item

    return retdata


def main():
    # loadSwipe()
    # loadnetwork()
    loadchunktraces()
    tmp = 0
    # build structure for buffer tracking

    # code to load the real trace

    # simulate the rebuffering event without running the real clock (global ts variable)

    # code to send the request to the server for every structure


    # r = requests.post("http://localhost:8333", data={'number': 12524, 'type': 'issue', 'action': 'show'})
    # print(r.status_code, r.reason)
    # print(r.text)

    # var data = {'nextChunkSize': bitrates, 'Type': 'BB', 'lastquality': last_quality, 'buffer': buffer, 'bandwidthEst': bandwidthEst, 'lastRequest': lastRequestedv, 'RebufferTime': rebuffer, 'lastChunkFinishTime': lastChunkFinishTime, 'lastChunkStartTime': lastChunkStartTime, 'lastChunkSize': lastChunkSize, 'playerId': playerId, 'currentPlayerIdx': currentPlayerIdx, 'url': url};
    # xhr.send(JSON.stringify(data));


if __name__ == "__main__":
    main()
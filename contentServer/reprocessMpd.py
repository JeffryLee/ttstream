import xml.etree.ElementTree as ET
from xml.etree import ElementTree as etree

import os


dataDir = "/home/acer/Documents/ttstream/contentServer/dash/data/"
fileList = os.listdir(dataDir)

# tmp = 0
etree.register_namespace("", "urn:mpeg:dash:schema:mpd:2011")

fileList = fileList[0:2]


print(fileList)

for folderName in fileList:

    if folderName[0] == ".":
        continue

    tree = ET.parse(dataDir+folderName+"/manifest.mpd")
    root = tree.getroot()

    for i in range(len(root[1])):
        AdaptationSet = root[1][i]

        if (AdaptationSet.attrib['contentType'] != "video"):
            continue

        Representation = root[1][i][0]
        SegmentTemplate = root[1][i][0][0]
        SegmentTimeline = root[1][i][0][0][0]

        timescale = int(SegmentTemplate.attrib['timescale'])
        duration = int(SegmentTimeline[0].attrib['d'])

        count = 1
        if 'r' in SegmentTimeline[0].attrib.keys():
            count += int(SegmentTimeline[0].attrib['r'])

        # chunk length in seconds
        chunkLength = duration/timescale

        bitrate_max = 0
        for j in range(1, count+1):

            fileName = dataDir+folderName+"/"+"""chunk-stream%d-%05d.m4s""" % (i, j)

            fsize = os.path.getsize(fileName)

            bitrate = fsize * 8 / chunkLength

            bitrate_max = max(bitrate_max, bitrate)

        root[1][i][0].attrib['bandwidth'] = str(int(bitrate_max))

        outstr = ET.tostring(root, encoding="utf8", method="xml")

        fd = open(dataDir+folderName+"/manifest-back.mpd", "wb")
        fd.write(outstr)
        fd.close()







        #     print(bitrate)
        #
        # print("===========")


        # print(root[1][i][0].attrib['bandwidth'])
        #
        # print(root[1][i][0])

        # os.path.getsize("/path/isa_005.mp3")

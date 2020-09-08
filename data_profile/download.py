from TikTokApi import TikTokApi
import os
api = TikTokApi()


for iteration in range(200):

    results = 2000

    trending = api.trending(count=results)


    savepath = "./video/"

    cnt = 0

    for tiktok in trending:
        # Prints the text of the tiktok
        print(tiktok['video']['downloadAddr'])


        filename = savepath+"%s.mp4"%tiktok['id']

        if os.path.exists(filename) == False:
            tmp = api.get_Video_By_DownloadURL(tiktok['video']['downloadAddr'])
            f = open(filename, 'wb')
            f.write(tmp)
            f.close()

        else:
            print("skip %d" %cnt)


        print("%d %d"%(iteration, cnt))
        cnt += 1


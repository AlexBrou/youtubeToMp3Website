import tornado.ioloop
import tornado.web
import youtube_dl
import random
import os
import json


def youtubeDownloadMp3(link, soundFormat):
    # title=str(random.randint(111111111,999999999))+"."+soundFormat

    # fileName=""
    # with youtube_dl.YoutubeDL() as ydl:
    #    ydl = youtube_dl.YoutubeDL()
    #    result = ydl.extract_info(link,download=False)
    #    fileName=result["title"]+"."+str(soundFormat)
    #fileName = fileName.replace(" ","_")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': soundFormat,
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ff = ydl.extract_info(link)
        title = ff["title"]
    return title



def cleanFile(filename):
    print("REMOVING: ", filename)
    os.remove(filename)


def searchFilename(title, soundFormat):
    fls = os.listdir()
    for fn in fls:
        if title in fn and "."+soundFormat in fn:
            return fn
    return None


class CORSHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header('Access-Control-Allow-Credentials', 'true')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()


class YoutubeToMp3(CORSHandler):

    def get(self):

        youtubeLink = self.get_argument('youtubeLink')
        soundFormat = self.get_argument('soundFormat')

        #youtubeLink = args["url"]
        title = youtubeDownloadMp3(youtubeLink, soundFormat)
        filename = searchFilename(title, soundFormat)
        self.set_header('Content-Type', 'application/octet-stream')
        self.set_header('Content-Disposition',
                        'attachment; filename=' + filename)
        print(filename)
        buf_size = 4096
        with open(filename, 'rb') as f:
            while True:
                data = f.read(buf_size)
                if not data:
                    break
                self.write(data)
        self.finish()
        print("file sent, now cleaning")
        cleanFile(filename)


def make_app():
    return tornado.web.Application([
        (r"/youtubeToMp3", YoutubeToMp3)
    ])


def main():
    app = make_app()
    app.listen(8888)

    tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":
    print("http://localhost:8888/youtubeToMp3?youtubeLink=https://www.youtube.com/watch?v=VWGu8v_6TMQ")

    main()

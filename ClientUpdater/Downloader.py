from urllib.request import HTTPPasswordMgrWithDefaultRealm
from urllib.request import HTTPBasicAuthHandler
from urllib.request import build_opener
from urllib.request import install_opener
from urllib.request import urlretrieve
from urllib.request import urlopen
from urllib.request import Request
from urllib.request import HTTPError
from pathlib import Path
from datetime import datetime
import time
import os
import Config
import hashlib


class Downloader:

    @staticmethod
    def checkForUpdate():
        print("Checking for updates")
        elements = Config.parseconfig()
        for e in elements:
            Downloader.isFileUpdated(e.link, e.sha)

    @staticmethod
    def initialize():
        if not os.path.isdir(Config.clientdir):
            os.makedirs(Config.clientdir)

        manifestfile = Path(Config.clientdir + "config2.xml")
        # TODO: Make authentication an option...
        if Config.authenticationRequired:
            Downloader.authenticate(Config.username, Config.password)

        # Download a new copy of the manifest file
        try:
            urlretrieve(Config.manifesturl, Config.clientdir + "manifest.xml")
        except HTTPError:
            print("Failed to authenticate")

        if not os.path.isdir(Config.clientdir):
            os.makedirs(Config.clientdir)

        if not os.path.isdir(Config.updaterdir):
            os.makedirs(Config.updaterdir)
        # Lets download the background and music...

        backgroundfile = Path(Config.updaterdir + "background.jpg")
        #musicfile = Path(Config.updaterdir + "bgmusic.mp3")
        #loadingfile = Path(Config.updaterdir + "background.jpg")

        if Config.bgdownload:
            try:
                Downloader.isFileUpdated(Config.weburl + 'updater/background.jpg', Config.updaterdir)
            except HTTPError:
                print("Failed to download background.")

        #try:
            #Downloader.isFileUpdated(Config.weburl + 'updater/bgmusic.mp3', Config.updaterdir)
        #except HTTPError:
            #print("Failed to download music.")



        #try:
            #Downloader.isFileUpdated(Config.weburl + 'updater/loading.gif', Config.updaterdir)
        #except HTTPError:
            #print("Failed to download loading.")

    @staticmethod
    def authenticate(username, password):
        passmanager = HTTPPasswordMgrWithDefaultRealm()  # None, 'url', 'username', 'pwd')
        passmanager.add_password(None, Config.weburl, username,
                                 password)

        auth_manager = HTTPBasicAuthHandler(passmanager)
        opener = build_opener(auth_manager)
        install_opener(opener)


    @staticmethod
    def isFileUpdated(filename, sha):
        file = Path(Config.clientdir + filename)
        # If the file exists, and the sha is different than that in the manifest, update.
        if file.is_file():
            oldsha = Downloader.getSHA(Config.clientdir, filename)
            print("filename: " + filename)
            print("sha: " + sha)
            print("oldsha: " + oldsha)
            if oldsha != sha:
                print("sha does not match, downloading...")
                Downloader.downloadFile(filename)
        else:  # Else if the file doesn't exist at all, download it.
            print("File does not exist, downloading it...")
            Downloader.downloadFile(filename)

    # This is the old way of checking if a file needs updating based upon unix timestamps of the file on the server.
    @staticmethod
    def isFileUpdatedOld(link, dir):
        # When given a link, Check if file exists on the Computer, else download it
        # if it is on the PC check the modified date vs website

        # Grab file name from the link
        filename = link[link.rfind('/') + 1:]
        file = Path(dir + filename)
        urlunixtime = Downloader.getUnixTimeFromUrl(link)

        # Can't check the file, so return instead of erroring.
        if urlunixtime == -1:
            return

        print("Checking: " + link)

        if file.is_file():
            fileunixtime = os.path.getmtime(dir + '\\' + filename)
            # See if the file on the server is newer
            print(urlunixtime > fileunixtime)
            print(urlunixtime)
            print(fileunixtime)

            if urlunixtime > fileunixtime:
                Downloader.downloadFile(link, dir)
        else:
            Downloader.downloadFile(link, dir)
            os.utime(dir + '\\' + filename, (urlunixtime, urlunixtime))

    @staticmethod
    def downloadFile(filename):
        print("Downloaded: " + filename)
        urlretrieve(Config.weburl + filename, Config.clientdir + '\\' + filename)


    # This is the old way I used to update, based upon Unix time before I switched over to sha and a manifest file.
    @staticmethod
    def getUnixTimeFromUrl(link):
        month = {
            'jan': 1, 'feb': 2, 'mar': 3, 'apr': 4, 'may': 5, 'jun': 6,
            'jul': 7, 'aug': 8, 'sep': 9, 'oct': 10, 'nov': 11, 'dec': 12}
        req = Request(link)
        try:
            handler = urlopen(req)
        except HTTPError:
            return -1

        modified = str(handler.info().get("Last-Modified"))
        split = modified.split()
        d = datetime(year=int(split[3]), month=month[split[2].lower()], day=int(split[1]), hour=int(split[4][0:2]),
                     minute=int(split[4][3:5]), second=int(split[4][6:8]))
        return time.mktime(d.timetuple())

    # Generates the sha of a file, not too concerned with ram usage, so I won't bother buffering this.
    @staticmethod
    def getSHA(dir, file):
        return hashlib.sha1(open(dir + file, 'rb').read()).hexdigest()


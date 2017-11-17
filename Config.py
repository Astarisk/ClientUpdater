import xml
import os
import logging
import platform
from pathlib import Path


# Parses the config file grabbing the download links needed based on architecture and os.
# Hopefully this works, Don't have all the machines needed to test this thoroughly

# Logging set up
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# OS variables
homedir = os.path.expanduser('~')
clientdir = homedir + '\TestClient\\bin\\'
weburl = 'https://raw.githubusercontent.com/Astarisk/ClientUpdater/master/ClientUpdater/testfiles/'
updaterdir = clientdir + "updater\\"
manifesturl = 'https://raw.githubusercontent.com/Astarisk/ClientUpdater/master/ClientUpdater/testfiles/manifest.xml'

# GUI variables
# Enables / Disables authentication, hiding the pw and username fields.
authenticationRequired = False
username = ''
password = ''

# Option to enable downloading of the updater background and music from the webserver.
# This option is needed if the python project is going to be converted into an exe. It makes things easier that way.
bgdownload = False

if not os.path.isdir(clientdir):
    os.makedirs(clientdir)

# Parses the manifest file, saving all the child nodes as an item class in a list
def parseconfig():
    os = platform.system()
    arch = platform.machine()

    tree = xml.etree.ElementTree.parse(clientdir + "manifest.xml")
    root = tree.getroot()
    elements = []
    for child in root:
        if (child.get("os") == os) | (child.get("os") is None):
            if (child.get("arch") == arch.lower()) | (child.get("arch") is None):
                elements.append(Item(child.get("os"), child.get("arch"), child.get("link"), child.get("sha")))
    logger.info(str(elements))
    return elements


# Saves the password.
def savepassword(pw):
    pwfile = open(clientdir + "pwfile", "w+")
    pwfile.write(pw)
    pwfile.close()


# Retrieves the saved password.
def getpassword():
    logger.info(clientdir + "pwfile")
    pwfile = Path(clientdir + "pwfile")

    if pwfile.is_file():
        return pwfile.read_bytes().decode('ascii')
    else:
        return ''


# Saves the username.
def saveusername(pw):
    usernamefile = open(clientdir + "usernamefile", "w+")
    usernamefile.write(pw)
    usernamefile.close()


# Retrieves the saved username.
def getusername():
    logger.info(clientdir + "usernamefile")
    usernamefile = Path(clientdir + "usernamefile")

    if usernamefile.is_file():
        return usernamefile.read_bytes().decode('ascii')
    else:
        return ''

# Saves the heap selection.
def saveheap(heap):
    heapfile = open(clientdir + "heapfile", "w+")
    heapfile.write(str(heap))
    heapfile.close()

# Retrieves the saved heap selection
def getheap():
    heapfile = Path(clientdir + "heapfile")
    if heapfile.is_file():
        if heapfile.read_bytes().decode('ascii') == '':
            return 0
        return heapfile.read_bytes().decode('ascii')
    else:
        return 0


# Saves the mute music option
def saveMute(mute):
    mutefile = open(updaterdir + "mutefile", "w+")
    mutefile.write(str(mute))
    mutefile.close()

# Retrieves the saved mute music option
def getMute():
    mutefile = Path(updaterdir + "mutefile")
    if mutefile.is_file():
        s = mutefile.read_bytes().decode('ascii')
        if s == 'True':
            return True
        else:
            return False
    else:
        return False

# An item for the xml parsing, an easy way to save the relevant data.
class Item:
    def __init__(self, oss, arch, link, sha):
        self.oss = oss
        self.arch = arch
        self.link = link
        self.sha = sha

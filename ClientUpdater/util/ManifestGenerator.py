import os
import hashlib
from pathlib import Path
import pysftp
import xml
import xml.etree.cElementTree as ET

# This tool will be used on a windows OS, specifically the folder for generation is on my desktop.
# The purpose of this script is just to generate a new manifest file, and uploads any changed files to the server
# The manifest file is just an xml file, I tried to make this as configurable and reusable as possible, but it still
# has some elements hard coded in to deal with special download cases. In particular OS and Arch specific downloads.
# The generator looks for a special case file, if it exists it'll just copy the handmade xml from that. The rest of the
# xml is auto generated...

# OS variables
homedir = os.path.expanduser('~')
filedir = '\\\Desktop\\ClientUpdate\\'  #C:\Users\Keith\Desktop\ClientUpdate

# sftp variables
hostname = '127.0.0.1'
username = 'Keith'
password = 'SuperSecretPassword'
sftpdir = 'C:\\Users\\Keith\\Desktop\\ClientUpdate'

# File related variables
files = os.listdir(homedir + filedir)
folders = []    # TODO: Add support for downloading files from other sub folders
specialcasedir = homedir + filedir + '\\lib\\'
specialcasefile = Path(specialcasedir + 'specialcase.xml')

print(specialcasefile)
# Calculates the SHA of a file
def getSHA(dir, file):
    return hashlib.sha1(open(dir + file, 'rb').read()).hexdigest()


for f in files:
    # Remove the manifest from the files list, its always uploaded to the server.
    if f == 'manifest.xml':
        files.remove(f)
    # Removing the folders from the file list, along with the manifest file itself as it's always changing.
    if os.path.isdir(homedir + filedir + f):
        files.remove(f)
print(files)

# Grab the old manifest file so we can compare it to the new one, which we will use to determine what files to send to
# the server.
oldmanifestfile = Path(homedir + filedir + "manifest.xml",)
oldtree = None
oldroot = None
if oldmanifestfile.is_file():
    oldmanifestfile = oldmanifestfile.read_bytes().decode('ascii')
    oldtree = xml.etree.ElementTree.parse(homedir + filedir + 'manifest.xml')
    oldroot = oldtree.getroot()

oldmanifest = []
if oldroot is not None:
    for child in oldroot:
        oldmanifest.append((child.get('link'), child.get('sha')))

# Generates the manifest.xml2
# Can't think of a better way to deal with OS and Arch versions aside from doing a custom special cases file
# So that is what I'm going to do for now....
root = None

# This is really nasty code... I need to find a better solution in the future that can support multiple OS and arch
if specialcasefile.is_file():
    temptree = xml.etree.ElementTree.parse(specialcasefile)
    root = temptree.getroot()

    for child in root:
        name = child.get('link')
        child.attrib['sha'] = getSHA(specialcasedir, name)
        print(child.attrib)
else:
    root = ET.Element("root")

for f in files:
    ET.SubElement(root, "item", link=f, sha=getSHA(homedir + filedir, f))

tree = ET.ElementTree(root)
tree.write(homedir + filedir + "manifest.xml")
newmanifest = []
for child in root:
    newmanifest.append((child.get('link'), child.get('sha')))

# produces the difference between the two sets, which would be the files that have been updated or changed
changes = list(set(oldmanifest) - set(newmanifest))

# Time to sftp and upload the changed files...
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None    # disable host key checking.
with pysftp.Connection(hostname, username=username, password=password, cnopts=cnopts) as sftp:
    with sftp.cd(sftpdir):             # Changes directory for sftp
        for x in changes:
            sftp.put(homedir + filedir + x[0])      # Uploads an updated file
        sftp.put(homedir + filedir + 'manifest.xml')    # Upload a new manifest file

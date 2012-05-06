import urllib
import os
import re
from sys import exit

base_dir = os.path.join(os.path.join(os.path.expanduser("~"),"Pictures"),'imgur')
#========================================================================

def download(url,img_dir): #Downloads a imgur file. Returns the file handle!
    url += ".jpg"
    filename = os.path.join(img_dir,url[-9:])
    
    fhandle = urllib.urlretrieve(url,filename)
    return fhandle

#download("http://i.imgur.com/NbL30.jpg",img_dir = base_dir) #Works!

#========================================================================

def get_album(album_url):
    source_code = urllib.urlopen(album_url).read()
    pattern = re.findall(pattern="<img class=\"unloaded\" data-src=\"http://i.imgur.com/[^.]*[.]",string=source_code)#..........
    tags = [tag.split()[-1].split("=")[-1][1:-1] for tag in pattern]

    destination = os.path.join(base_dir,album_url[-5:])

    if os.path.isdir(destination):
        return
    if not os.path.isdir(destination):
        os.mkdir(destination)


    for url in tags:
        print "Downloading '%s'..." % url
        download(url,destination)



def download_albums(album_urls):
    
    if not os.path.isdir(base_dir):
        os.mkdir(base_dir)


    for album_url in album_urls:
        get_album(album_url)
        print "="*72
        print "Finished downloading '%s'!" % album_url
        print "="*72


album_url = ["http://imgur.com/a/FV3RG", "http://imgur.com/a/0kI4G","http://imgur.com/a/bvd5r"]
download_albums(album_url)

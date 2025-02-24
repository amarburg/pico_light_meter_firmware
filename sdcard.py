
import sdcardio
import storage
import board
import busio
import os

class SdCard:

    def __init__(self, spi):
        cs = board.GP17

        sdcard = sdcardio.SDCard(spi, cs)
        vfs = storage.VfsFat(sdcard)

        storage.mount(vfs, "/sd")

        with open("/sd/test.txt", "w") as f:
           f.write("Hello world!\r\n")

    def print_directory(self, path="/sd", tabs=0):
        for file in os.listdir(path):
            if file == "?":
                continue  # Issue noted in Learn
            stats = os.stat(path + "/" + file)
            filesize = stats[6]
            isdir = stats[0] & 0x4000

            if filesize < 1000:
                sizestr = str(filesize) + " by"
            elif filesize < 1000000:
                sizestr = "%0.1f KB" % (filesize / 1000)
            else:
                sizestr = "%0.1f MB" % (filesize / 1000000)

            prettyprintname = ""
            for _ in range(tabs):
                prettyprintname += "   "
            prettyprintname += file
            if isdir:
                prettyprintname += "/"
            print('{0:<40} Size: {1:>10}'.format(prettyprintname, sizestr))

            # recursively print directory contents
            if isdir:
                self.print_directory(path + "/" + file, tabs + 1)
__author__ = 'matt'

class Song(object):
    def __init__(self, inLyrics):
        self.lyrics = inLyrics

    def sing_me_a_song(self):
        for line in self.lyrics:
            print line

myLyrics = "la la la la la la la la"

mySong = Song(myLyrics)

if __name__ == '__main__':
    print mySong.sing_me_a_song()

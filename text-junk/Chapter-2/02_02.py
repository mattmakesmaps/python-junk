import fileinput
import enchant

from enchant.tokenize import get_tokenizer
from enchant.tokenize import HTMLChunker

# Tell Python that we only want new-style classes.
# I don't know how widely this is used over
# class name(object):
__metaclass__ = type

class HTMLSpellChecker:
    def __init__(self, lang='en_US'):
        """
        Setup tokenizer.
        """
        self.lang = lang
        self._dict = enchant.Dict(self.lang)
        self._tk = get_tokenizer(self.lang, chunkers=(HTMLChunker,))

    def __call__(self, line):
        for word,off in self._tk(line):
            if not self._dict.check(word):
                # Yield will return value as soon as it is hit
                # Loop will continue going.
                yield word, self._dict.suggest(word)

if __name__ == '__main__':

    check = HTMLSpellChecker()
    for line in fileinput.input():
        # Since HTMLSpellChecker's __call__ method only yields return values
        # when a word is mispelled, this block will only execute when
        # mispellings occur.
        for word,suggestions in check(line):
            print "error on line %d (%s) in file %s. Did you mean:\n\t%s" % \
            (fileinput.filelineno(), word, fileinput.filename(),
                ', '.join(suggestions))

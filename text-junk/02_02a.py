import sys
import urllib2
import enchant
import optparse

from enchant.tokenize import get_tokenizer
from enchant.tokenize import HTMLChunker

class HTMLSpellChecker(object):
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
    parser = optparse.OptionParser()
    parser.add_option('-u', '--url', help="URL to Check")
    opts, args = parser.parse_args()

    if not opts.url:
        parser.error("URL is required")

    check = HTMLSpellChecker()
    try:
        source = urllib2.urlopen(opts.url)
    except urllib2.URLError, e:
        # Using str(e), then trying to get str(e.reason)
        # is an example of duck typing.
        reason = str(e)
        # If the error has a reason attribute,
        # defer to that instead. Else, use str
        # of exception instance.
        try:
            reason = str(e.reason)
        except AttributeError:
            pass

        print >>sys.stderr, "File Download Error: %s" % reason
        sys.exit(-1)

    # Can't we just use source here?
    for line in source:
        lineno = 0
        for word, suggestions in check(line):
            lineno += 1
            print "error on line %d (%s) on page %s. Did you mean:\n\t%s" % \
                  (lineno, word, opts.url, ', '.join(suggestions))

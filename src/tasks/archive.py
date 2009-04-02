import sys
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)

class Archive(object):
    def __init__(self, *args, **kwargs):
        self._archive = {}
        super(Archive, self).__init__(*args, **kwargs)

    def add(self, article):
        self._archive[article.year] = \
            self._archive.get(article.year, {})
        self._archive[article.year][article.month] = \
            self._archive[article.year].get(article.month, {})
        self._archive[article.year][article.month][article.day] = \
            self._archive[article.year][article.month].get(article.day, []) + [article]

    @property
    def current(self):
        return self._archive.copy()


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'archive')
    archive = Archive()
    map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    
    print "Archive:", archive.current

def help(args):
    print "Build the archive of published articles"
    print util.get_help(OPTIONS, prog = 'archive')
    

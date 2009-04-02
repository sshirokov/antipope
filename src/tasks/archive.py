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
        if self._archive[article.year][article.month][article.day].count(article) > 1:
            self._archive[article.year][article.month][article.day].remove(article)
            return False
        return article

    @property
    def current(self):
        return self._archive.copy()

    def years(self):
        return self.current.keys()
    def months(self, year):
        return self.current.get(year, {}).keys()
    def days(self, year, month):
        return self.current.get(year, {}).get(month, {}).keys()
    def articles(self, year, month, day):
        return self.current.get(year, {}).get(month, {}).get(day, [])

    def all(self, year = None, month = None, day = None):
        for year_k, year_v in self.current.items():
            if year == None or year_k == year:
                for mon_k, mon_v in year_v.items():
                    if month == None or mon_k ==  month:
                        for day_k, day_l in mon_v.items():
                            if day == None or day_k == day:
                                for article in day_l:
                                    yield article


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'archive')
    archive = Archive()
    map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    
def help(args):
    print "Build the archive of published articles"
    print util.get_help(OPTIONS, prog = 'archive')
    

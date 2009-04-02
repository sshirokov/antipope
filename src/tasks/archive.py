import sys, os
import jinja2
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)

class Archive(object):
    ARCHIVE_TEMPLATE = 'archive.html'
    
    def __init__(self, *args, **kwargs):
        self._archive = {}
        template_path = os.path.abspath(config.settings.TEMPLATE_DIR)
        self.jenv = jinja2.Environment(loader = jinja2.FileSystemLoader(template_path))
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
        return sorted(self.current.keys())
    def months(self, year):
        return sorted(self.current.get(year, {}).keys())
    def days(self, year, month):
        return sorted(self.current.get(year, {}).get(month, {}).keys())
    def articles(self, year, month, day):
        return Slicer.sort(self.current.get(year, {}).get(month, {}).get(day, []))

    def all(self, year = None, month = None, day = None):
        for year_k, year_v in self.current.items():
            if year == None or year_k == year:
                for mon_k, mon_v in year_v.items():
                    if month == None or mon_k ==  month:
                        for day_k, day_l in mon_v.items():
                            if day == None or day_k == day:
                                for article in day_l:
                                    yield article

    def render(self, objects, href_template, name_func = str, href_func = lambda i: i):
        links = [dict(name = name_func(item),
                      href = href_template % href_func(item))
                 for item in objects]
        return self.jenv.get_template(self.ARCHIVE_TEMPLATE).render(links = links)

    def build_one(self, base, content):
        archive_file = 'archive.html'
        archive_path = os.path.join(base, archive_file)
        try: os.makedirs(base)
        except OSError, e:
            if e.errno != 17: raise
        archive_dest = open(archive_path, "w")
        archive_dest.write(content)
        archive_dest.close()
        return archive_path

    def build(self, dest, options):
        base = os.path.join(dest, "archive")
        archive_file = "archive.html"
        
        base_href = '/archive/%s'
        self.build_one(base, self.render(self.years()[-1::-1], base_href))
        
        for year in self.years():
            year_base = os.path.join(base, str(year))
            year_href_base = (base_href % year) + "/%s"
            self.build_one(year_base,
                           self.render(self.months(year),
                                       year_href_base,
                                       name_func = util.month_name,
                                       href_func = lambda m: "%02d" % m))
            for month in self.months(year):
                month_base = os.path.join(year_base, "%02d" % month)
                self.build_one(month_base,
                           self.render(Slicer.sort(self.all(year, month), desc = True),
                                       href_template = '/%s',
                                       href_func = lambda a: a.path,
                                       name_func = lambda a: a.name))
                    


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'archive')
    archive = Archive()
    articles = map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    if not options.quick:
        print "WARNING: Build refresh not implemented"
    archive.build(config.settings.OUTPUT_BASE, options)
    
def help(args):
    print "Build the archive of published articles"
    print util.get_help(OPTIONS, prog = 'archive')
    

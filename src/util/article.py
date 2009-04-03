import os, re
import yaml
from config import settings
from util.parser import Parser, ParserError
from util.slicer import Slicer
from util import ObjDict

class ArticleError(Exception): pass
class ArticleSystemError(ArticleError): pass

class Article(object):
    '''
    Factory and representation of an Article.
    '''
    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        try: self.meta = ObjDict(Parser.get_meta(slug))
        except ParserError, e: raise ArticleError("Cannot get data for article")

    @property
    def name(self):
        return self.meta.get('name', "*Untitled*")

    @property
    def date(self):
        from dateutil.parser import parser
        from datetime import datetime
        if not self.meta.has_key('date'):
            self.meta.date = datetime.fromtimestamp(
                os.stat(os.path.join(settings.POST_ROOT, self.slug)).st_mtime).isoformat()
            self.save()
        return parser().parse(self.meta.date)

    @property
    def compiled(self):
        output_file = os.path.join(self.get_path('output', 'absolute'), 'article.html')
        if not os.path.isfile(output_file) and not self.build(settings.OUTPUT_BASE):
            raise ArticleError("Do not have, and cannot build compiled output: %s" % output_file)
        try:
            output_f = open(output_file)
            output = output_f.read()
            output_f.close()
        except IOError: raise ArticleError("Cannot read compiled output: %s" % output_file)
        return output
            
    @property
    def year(self): return self.date.year
    @property
    def month(self): return self.date.month
    @property
    def day(self): return self.date.day

    @property
    def path(self): return self.get_path()
    
    def get_path(self, type = 'url', style = 'relative'):
        stderror = lambda type, style, message = '': ArticleSystemError("Cannot return a path of %s/%s%s" % (type, style, message and ": %s" % message))
        if not (type in ('url', 'os', 'output') and style in ('relative', 'absolute')): raise stderror(type, style)
        if type == 'url':
            if style == 'absolute':
                try: return "%s/%s" % (settings.BASE_URL, self.get_path('url', 'relative'))
                except AttributeError: raise stderror(type, style, "No settings.BASE_URL")
            elif style == 'relative':
                return "/".join([str(self.date.year),
                                    self.date.strftime("%m"),
                                    self.date.strftime("%d"),
                                    self.slug])
        if type == 'output':
            if style == 'relative': return os.path.join(settings.OUTPUT_BASE,
                                                        self.get_path('url', 'relative').replace('/', os.path.sep))
            if style == 'absolute': return os.path.abspath(self.get_path('output', 'relative'))
        elif type == 'os':
            if style == 'absolute': path = os.path.abspath(self.get_path('os', 'relative'))
            elif style == 'relative': path = os.path.join(settings.POST_ROOT, self.slug)
            return path

    def generate(self):
        main = os.path.join(self.get_path('os', 'absolute'), settings.POST_FILE)
        main_safe = main.replace('"', '\\"')
        outfile = re.sub('\.org$', '.html', main)
        cmd = '%(emacs)s --batch --load ~/.emacs --visit="%(file)s" --funcall org-export-as-html-batch' % dict(emacs = settings.EMACS_BIN,
                                                                                                                                        file = main_safe)
        output_data = None
        
        if os.path.isfile(main) and os.system(cmd) == 0 and os.path.isfile(outfile):
            try:
                output = open(outfile)
                output_data = output.read()
                output.close()
                try: os.unlink(outfile)
                except OSError: pass
            except IOError: raise ArticleError("Unable to read article output")
        else:
            raise ArticleError("Command did not succeed or outfile was not generated.")
        return output_data

    def build(self, dest):
        from BeautifulSoup import BeautifulSoup
        try: base_html = self.generate()
        except ArticleError: return None
        
        if base_html:
            output_soup = BeautifulSoup(base_html)
            try: os.makedirs(os.path.join(dest, self.path))
            except OSError, e:
                if e.errno != 17: raise ArticleError("Unable to create output path")
            try:
                output = open(os.path.join(dest, self.path, 'article.html'), "w")
                output.write(output_soup.body.contents[1].renderContents())
                output.close()
            except IOError: raise ArticleError("Unable to open output location")
            return True
        else:
            return False

    def save(self):
        try:
            meta_path = os.path.join(settings.POST_ROOT, self.slug, settings.META_FILE)
            data = yaml.dump(self.meta.to_dict(),
                             default_flow_style = False,
                             explicit_start = True)
            meta = open(meta_path + ".swp", "w")
            meta.write(data)
            meta.close()
            os.rename(meta_path + ".swp", meta_path)
        except yaml.YAMLError: return False
        except IOError: return False
        except OSError:
            try: os.unlink(meta_path + ".swp")
            except OSError: pass
            return False
        else: return True

    def __repr__(self):
        return "%s/'%s'" % (self.slug, self.meta.name or "*Untitled*")

    @classmethod
    def find(slug):
        '''
        Find an article by slug
        '''
        return slug in Slicer.slices.all() and self(slug)

import os
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
    def path(self): return self.get_path()
    
    def get_path(self, type = 'url', style = 'relative'):
        stderror = lambda type, style, message = '': ArticleSystemError("Cannot return a path of %s/%s%s" % (type, style, message and ": %s" % message))
        if not (type in ('url', 'os') and style in ('relative', 'absolute')): raise stderror(type, style)
        if type == 'url':
            if style == 'absolute':
                try: return "%s/%s" % (settings.BASE_URL, self.get_path('url', 'relative'))
                except AttributeError: raise stderror(type, style, "No settings.BASE_URL")
            elif style == 'relative':
                return "/".join([str(self.date.year),
                                    self.date.strftime("%m"),
                                    self.date.strftime("%d"),
                                    self.slug])
        elif type == 'os':
            if style == 'absolute': return os.path.join(os.getcwd(), self.get_path('os', 'relative'))
            elif style == 'relative': return os.path.join(settings.POST_ROOT, self.slug)
    
    def build(self, dest):
        return True

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

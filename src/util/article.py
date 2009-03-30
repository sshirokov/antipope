import os
from config import settings
from util.parser import Parser, ParserError
from util.slicer import Slicer
from util import ObjDict

class ArticleError(Exception): pass

class Article(object):
    '''
    Factory and representation of an Article.
    '''
    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        try: self.meta = ObjDict(Parser.get_meta(slug), default = False)
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
        return parser().parse(self.meta.date)
    
    def build(self, dest):
        return True

    def __repr__(self):
        return "%s/'%s'" % (self.slug, self.meta.name or "*Untitled*")

    @classmethod
    def find(slug):
        '''
        Find an article by slug
        '''
        return slug in Slicer.slices.all() and self(slug)

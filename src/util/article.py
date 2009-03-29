from util.parser import Parser
from util.slicer import Slicer
from util import ObjDict

class ArticleError(Exception): pass

class Article(object):
    '''
    Factory and representation of an Article.
    '''
    def __init__(self, slug, *args, **kwargs):
        self.slug = slug
        self.meta = ObjDict(Parser.get_meta(slug), default = False)

    @classmethod
    def find(slug):
        '''
        Find an article by slug
        '''
        return slug in Slicer.slices.all() and self(slug)

import os
import yaml
from yaml.error import YAMLError
from config import settings

class ParserError(Exception): 
    _STD_ERROR = "Error prasing for %(slug)s: %(error)s"

    @staticmethod
    def std(slug, error):
        return ParserError(ParserError._STD_ERROR % {'slug': slug,
                                                     'error': error})

class Parser(object):
    @classmethod
    def get_meta(self, slug):
        '''
        Returns a dict of article meta data for the given slug
        '''
        try: meta = open(os.path.join(settings.POST_ROOT, slug, settings.META_FILE))
        except IOError, e: raise ParserError.std(slug, e)
        else:
            try: data = yaml.load(meta)
            except YAMLError, e: raise (meta.close() or ParserError.std(slug, e))
            return meta.close() or data

    
    @classmethod
    def is_article(self, slug):
        try: return self.get_meta(slug) and True
        except ParserError: return False

    @classmethod
    def is_published(self, slug):
        try: return self.get_meta(slug).get('status', '-undef-') == 'published'
        except ParserError: return False

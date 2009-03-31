import os
from parser import Parser
from config import settings

class Slicer(object):
    @classmethod
    def sort(self, article_list, key = 'date'):
        return sorted(article_list,
                      lambda a1, a2: \
                          (getattr(a1, key) < getattr(a2, key) and -1) or \
                          (getattr(a1, key) == getattr(a2, key) and 0) or \
                          (getattr(a1, key) > getattr(a2, key) and 1))
    
    class slices:
        '''
        Contains the user-accessed slice returning methods
        All slice returning methods return lists of tags"
        '''
        @staticmethod
        def all():
            return filter(Parser.is_article, os.listdir(settings.POST_ROOT))


        @staticmethod
        def published():
            return filter(lambda a: \
                              Parser.is_article(a) and Parser.is_published(a),
                          os.listdir(settings.POST_ROOT))

import os
from parser import Parser
from config import settings

class Slicer(object):
    class slices:
        '''
        Contains the user-accessed slice returning methods
        All slice returning methods return lists of tags"
        '''
        @staticmethod
        def all():
            return filter(Parser.is_article, os.listdir(settings.POST_ROOT))


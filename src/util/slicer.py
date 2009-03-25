import os
import Parser

class Slicer(object):
    class slices:
        '''
        Contains the user-accessed slice returning methods
        All slice returning methods return lists of tags"
        '''
        @staticmethod
        def all():
            return filter(Parser.is_article, os.listdir(Slicer._POST_ROOT))
        

print "Slicer loaded"

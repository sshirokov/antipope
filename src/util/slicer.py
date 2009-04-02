import os
from parser import Parser
from config import settings

class Slicer(object):
    @classmethod
    def sort(self, article_list, key = 'date', desc = False):
        articles = sorted(article_list,
                      lambda a1, a2: \
                          (getattr(a1, key) < getattr(a2, key) and -1) or \
                          (getattr(a1, key) == getattr(a2, key) and 0) or \
                          (getattr(a1, key) > getattr(a2, key) and 1))
        return (desc and articles[-1::-1]) or articles

    @classmethod
    def slugs_to_articles(self, slug_list, prune = False):
        def convert(slug):
            from util.article import Article, ArticleError
            try: return Article(slug)
            except ArticleError: return None
        articles = map(convert, slug_list)
        if prune: articles = filter(None, articles)
        return articles
    
    class slices(object):
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

    class objects(object): pass

#Ugly, and should probably be done better, somehow
for method in filter(lambda s: '__' not in s, dir(Slicer.slices)):
    setattr(Slicer.objects, method, staticmethod(lambda *a, **k: Slicer.slugs_to_articles(getattr(Slicer.slices, method)(*a, **k), prune = True)))

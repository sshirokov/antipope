import os
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError
from util.archive import Archive

OPTIONS = (("dest", ("-d", "--dest"), dict(help = 'Overwrite build destination (Default: %default)',
                                                action = 'store',
                                                default = config.settings.OUTPUT_BASE)),
           ("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)

def build_main(dest, archive, options):
    '''
    Build the front page
    '''
    index_file = "index.html"
    index_path = os.path.join(dest, index_file)
    try:
        index = open(index_path, "w")
        index.write(archive.jenv.get_template("article_list.html").render(
                dict(articles = Slicer.sort(list(archive.all())[:5],
                                            desc = True))))
        index.close()
    except IOError, e: return False
    return True

def build_index(dest, article, archive, options):
    '''
    Builds the index page for the given article
    '''
    index_file = "index.html"
    index_path = index_path = os.path.join(article.get_path(type = 'output',
                                                            style = 'absolute'),
                                           index_file)
    try:
        index = open(index_path, "w")
        index.write(archive.jenv.get_template("article_index.html").render(
                dict(article = article)))
        index.close()
    except IOError, e: return None
    return article

def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'index')
    archive = Archive()
    articles = map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    print "All articles:", articles
    build_main(options.dest, archive, options)
    print "Indexed articles:", map(lambda a: build_index(options.dest, a, archive, options),
                                   articles)
    
    
def help(args):
    print "Build the index pages required."
    print util.get_help(OPTIONS, prog = 'index')
    

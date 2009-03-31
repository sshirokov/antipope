import sys
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("dest", ("-d", "--dest"), dict(help = 'Overwrite build destination (Default: %default)',
                                                action = 'store',
                                                default = config.settings.OUTPUT_BASE)),)


def build(slug, dest = config.settings.OUTPUT_BASE):
    try: article = Article(slug)
    except ArticleError: article = None
    print "Writing:", article or slug, "........",
    status = article and article.build(dest)
    print {None: "[Article Error]",
           False: "[Write Error]"}.get(status, "[Done]")
    return status and article

def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'build')
    articles = map(lambda slug: build(slug, options.dest),
                   Slicer.slices.published())

def help(args):
    print "Build output from 'published' article data."
    print util.get_help(OPTIONS, prog = 'build')
    

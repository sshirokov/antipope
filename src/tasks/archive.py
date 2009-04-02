import sys
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'archive')

def help(args):
    print "Build the archive of published articles"
    print util.get_help(OPTIONS, prog = 'archive')
    

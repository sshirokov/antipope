import sys, os
import jinja2
import config
import util
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("dest", ("-d", "--dest"), dict(help = 'Overwrite build destination (Default: %default)',
                                                action = 'store',
                                                default = config.settings.OUTPUT_BASE)),
           ("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)
def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'index')
    
def help(args):
    print "Build the index pages required."
    print util.get_help(OPTIONS, prog = 'index')
    

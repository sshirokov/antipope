import util
from util.slicer import Slicer

OPTIONS = ()

def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'build')
    articles = Slicer.slices.published()
    print ", ".join(articles)

def help(args):
    print "Build output from 'published' article data."
    print utils.get_help(OPTONS, prog = 'build')
    

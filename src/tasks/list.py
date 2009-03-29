import util
from util.slicer import Slicer
from util.parser import Parser
from util.article import Article

OPTIONS = (("name", ("-n", "--with-name"), dict(help = 'List slugs with full names',
                                                action = 'store_true',
                                                default = False)),)

def format_extra_data(slug, options):
    '''
    Return a string to supplement a listing with
    given a slug and the set of options.
    '''
    article, extra = Article(slug), ''
    if options.name: extra += '- "%s"' % article.meta.name or '*Untitled*'
    return extra

def run(args):
    '''
    List available blogs
    '''
    (options, args) = util.get_args(args, OPTIONS, prog = 'list')
    slices = Slicer.slices.all()
    if not len(slices): return
    for article in slices:
        print article, format_extra_data(article, options)
        

def help(args):
    print "Lists all available posts"
    print util.get_help(OPTIONS, prog = 'list')
    

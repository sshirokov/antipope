import util
from util.slicer import Slicer

OPTIONS = (
    ("name", ("-n", "--with-name"), dict(help = 'List slugs with full names',
                                         action = 'store_true',
                                         default = False)),)

def run(args):
    '''
    List available blogs
    '''
    (options, args) = util.get_args(args, OPTIONS, prog = 'list')
    slices = Slicer.slices.all()
    if not len(slices): return
    
    print '\n'.join(slices)

def help(args):
    print "Lists all available posts"
    print util.get_help(OPTIONS, prog = 'list')
    

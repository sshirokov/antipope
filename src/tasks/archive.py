import config
import util
from util.archive import Archive
from util.slicer import Slicer
from util.article import Article, ArticleError

OPTIONS = (("dest", ("-d", "--dest"), dict(help = 'Overwrite build destination (Default: %default)',
                                                action = 'store',
                                                default = config.settings.OUTPUT_BASE)),
           ("quick", ("-q", "--quick"), dict(help = 'Do not rebuild stale articles.',
                                                action = 'store_true',
                                                default = False)),)

                    


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'archive')
    archive = Archive()
    articles = map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    if not options.quick:
        print "WARNING: Build refresh not implemented"
    archive.build(options.dest, options)
    
def help(args):
    print "Build the archive of published articles"
    print util.get_help(OPTIONS, prog = 'archive')
    

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

def copy_media():
    import shutil
    shutil.rmtree(os.path.join(config.settings.OUTPUT_BASE, config.settings.MEDIA_DIR),
                  ignore_errors = True)
    shutil.copytree(config.settings.MEDIA_DIR, os.path.join(config.settings.OUTPUT_BASE,
                                                            config.settings.MEDIA_DIR))

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
    copy_media()
    return True

def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'index')
    archive = Archive()
    articles = map(archive.add, Slicer.sort(Slicer.objects.all(), desc = True))
    build_main(options.dest, archive, options)
    
    
def help(args):
    print "Build the index pages required."
    print util.get_help(OPTIONS, prog = 'index')
    

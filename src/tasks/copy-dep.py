import sys, os
import config
import util

OPTIONS = (("what", ("-a", "--all"), dict(help = "Copy all dependencies",
                                          const = ["all"],
                                          default = ['all'],
                                          action = "store_const")),
           ("what", ("-m", "--media"), dict(help = "Copy all media",
                                            const = "media",
                                            action = "append_const")),
           ("what", ("-l", "--linked"), dict(help = "Copy all linked files",
                                             const = "linked",
                                             action = "append_const")),)

def copy_media():
    import shutil
    shutil.rmtree(os.path.join(config.settings.OUTPUT_BASE, config.settings.MEDIA_DIR),
                  ignore_errors = True)
    shutil.copytree(config.settings.MEDIA_DIR, os.path.join(config.settings.OUTPUT_BASE,
                                                            config.settings.MEDIA_DIR))

def copy_all():
    copy_media()


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'copy-dep', options_func = lambda options:\
                                        (len(options.what) > 1 and (options.what[0] == 'all') and (options.what.remove('all') or options))\
                                             or options)
    if 'all' in options.what:
        print "-> Copying all"
        copy_all()
    elif 'all' not in options.what:
        if 'media' in options.what:
            print "-> Copying media"
            copy_media()
        if 'linked' in options.what:
            print "-> Copying linked"
            sys.stderr.write("WARNING: Linked copy doesn't exist.")
            pass #Copy linked
    print options, args

def help(args):
    print "Copy dependencies (media, linked files, etc.) to output"
    print util.get_help(OPTIONS, prog = 'copy-dep')


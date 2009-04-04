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


def run(args):
    (options, args) = util.get_args(args, OPTIONS, prog = 'copy-dep', options_func = lambda options:\
                                        (len(options.what) > 1 and (options.what[0] == 'all') and (options.what.remove('all') or options))\
                                             or options)
    print options, args

def help(args):
    print "Copy dependencies (media, linked files, etc.) to output"
    print util.get_help(OPTIONS, prog = 'copy-dep')


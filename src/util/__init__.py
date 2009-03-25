def _get_optparser(**kwargs):
    from optparse import OptionParser
    kwargs = dict({'add_help_option': False,},
                  **kwargs)
    return OptionParser(**kwargs)

def _apply_options(parser, options, req_args = ()):
    parser.set_usage('%%prog %(options)s%(args)s' % dict(args = ' '.join(req_args),
                                                          options = (options or '') and '[options] '))
    map(lambda op: parser.add_option(dest = op[0], *op[1], **op[2]), options)
    return parser

def get_help(options, req_args = ()):
    pass

def get_args(args, options = (), req_args = (), max_args = None):
    opts = _apply_options(_get_optparser(), options)
    (options, args) = opts.parse_args(args)
    if not (len(req_args) <= len(args)) and (max_args == None or max_args >= len(args)):
        opts.error("Wrong number of arguments.")
    return (options, args)

    

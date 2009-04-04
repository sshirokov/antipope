class ObjDict(dict):
    def __init__(self, *args, **kwargs):
        super(ObjDict, self).__init__(*args, **kwargs)
        for k, v in self.items():
            if type(v) == dict: self.update({k: ObjDict(v)})
            
    def to_dict(self):
        r_self = self.copy()
        for k, v in r_self.items():
            if type(v) == ObjDict: r_self.update({k: v.to_dict()})
        return r_self
            
    def __getattr__(self, key): return self[key]
    def __setattr__(self, key, value): self[key] = (type(value) == dict) and ObjDict(value) or value

def month_name(month):
    from datetime import datetime
    return datetime(datetime.now().year, month, datetime.now().day).strftime("%B")

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

def get_help(options = (), req_args = (), prog = 'command'):
    return _apply_options(_get_optparser(prog = prog), options, req_args).format_help()

def get_args(args, options = (), req_args = (), max_args = None, prog = 'command', options_func = lambda o: o, args_func = lambda a: a):
    opts = _apply_options(_get_optparser(prog = prog), options)
    (options, args) = opts.parse_args(['*self*'] + args)
    for spreader in filter(lambda arg: re.match('\.+$', arg), req_args):
        si = list(req_args).index(spreader)
        req_args = req_args[0:si] + req_args[si + 2:]
    if not (len(req_args) <= len(args)) and (max_args == None or max_args >= len(args)):
        opts.error("Wrong number of arguments.")
    return (options_func(options), args_func(args))

    

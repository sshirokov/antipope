#!/usr/bin/env python
import sys

class UserError(Exception): pass

def usage():
    print "Manage must be called with a command as an argument."
    sys.exit(0)

if __name__ == '__main__':
    self, args = sys.argv[0], sys.argv[1:]
    if len(args) < 1: usage()
    (command, args) = args[0], args[1:]

    if command == 'help' and ((len(args) > 0) or ussage()):
        try: __import__('tasks.%s' % args[0], globals(), locals(), ['tasks']).help(args[1:])
        except ImportError: raise UserError("No such command: %s" % args[0])
    else:
        try: __import__('tasks.%s' % command, globals(), locals(), ['tasks']).run(args)
        except ImportError: raise UserError("No such command: %s" % command)
        

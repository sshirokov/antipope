#!/usr/bin/env python
import sys, os, re, inspect
sys.path.append(os.path.join('..'))

class UserError(Exception): pass

def usage():
    print "Manage must be called with a command as an argument."
    sys.exit(0)
    
def main(self, args):    
    self, args = sys.argv[0], sys.argv[1:]
    if len(args) < 1: usage()
    (command, args) = args[0], args[1:]

    if command == 'help' and ((len(args) > 0) or usage()):
        try: __import__('tasks.%s' % args[0], globals(), locals(), ['tasks']).help(args[1:])
        except ImportError: raise UserError("No such command: %s" % args[0])
    else:
        try: __import__('tasks.%s' % command, globals(), locals(), ['tasks']).run(args)
        except ImportError, e:
            if re.match("No module named", e.message) and e.message.split(' ')[-1] == command:
                raise UserError("No such command: %s" % command)
            else: raise

    
if __name__ == '__main__':
    try: main(sys.argv[0], sys.argv[1:])
    except UserError, e: sys.stderr.write("%s\n" % e)
    
        

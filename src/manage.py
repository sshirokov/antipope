import sys
print "manage.py running"

class UserError(Exception): pass

if __name__ == '__main__':
    print "Manage running"
    (command, args) = sys.argv[0], sys.argv[1:]
    print "Command: '%s'" % command

    if command == 'help':
        if not(len(args) >= 1): raise UserError("Need arguments for help")
        try: __import__('tasks.%s' % args[0], globals(), locals(), ['tasks']).help(args[1:])
        except ImportError: raise UserError("No such command: %s" % args[0])
    else:
        try: __import__('tasks.%s' % command, globals(), locals(), ['tasks']).run(args)
        except ImportError: raise UserError("No such command: %s" % command)
        

        
    print "Manage completed"

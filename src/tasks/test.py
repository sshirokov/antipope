import util

def run(args):
    print "Testing command executed"
    print "\tArgs:", util.get_args(args, prog = 'test')

def help(args):
    print "Test help executed"
    print "Getting help:"
    print util.get_help(prog = 'test')

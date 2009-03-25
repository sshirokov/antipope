import util

def run(args):
    print "Testing command executed"
    print "\tArgs:", util.get_args(args)

def help(args):
    print "Test help executed"
    print "\targs(%s)" % args

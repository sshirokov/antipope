from util.slicer import Slicer

def run(args):
    '''
    List available blogs
    '''
    slices = Slicer.slices.all()
    if len(slices): print '\n'.join(Slicer.slices.all())

def help(args):
    print "Lists all available posts"
    

import sys
import auto

cmd_length = sys.argv.__len__()

if(cmd_length == 2):
    if(sys.argv[1] == '-h' or sys.argv[1] == '--help'):
        print("help message")
    elif(sys.argv[1] == 'clone_all'):
        auto.clone_all()
    elif(sys.argv[1] == 'pull_all'):
        auto.pull_all()
    elif(sys.argv[1] == 'debuild_all'):
        auto.debuild_all()
    elif(sys.argv[1] == 'checkout_all'):
        auto.checkout_all()
    elif(sys.argv[1] == 'do_all'):
        auto.pull_all()
        auto.build_all()
    elif(sys.argv[1] == 'do_all_debian'):
        auto.pull_all()
        auto.checkout_all()
        auto.build_all()


elif(cmd_length == 3):
    #clone dir
    if(sys.argv[1] == 'clone'):
        auto.clone(sys.argv[2])
    #debuild name
    if(sys.argv[1] == 'debuild'):
        auto.debuild(sys.argv[2])
    #pull name
    if(sys.argv[1] == 'pull'):
        auto.pull(sys.argv[2])
    if(sys.argv[1] == 'chekout'):
        auto.checkout(sys.argv[2])

from subprocess import check_call as run 
from getopt import getopt, GetoptError 
RELEASE = 'master' # default release 
SRC_DIR = "/storage/emulated/0/primateria" # checkout directory 
UPDATE_CMD = ('pip install --src="%s" --upgrade -e ' 
'git://github.com/KaiXtr/primateria.git@%s#egg=swork' 
)

def update(args): 
    try: 
        opts, args = getopt(args, 'sr:', ['sudo', 'src=', 'release=', 'commit=']) 
    except GetoptError as err: 
        log(err) 
        usage(error_codes['option'])

    sudo = False 
    src_dir = SRC_DIR 
    release = RELEASE 
    commit = None 
    for opt, arg in opts: 
        if opt in ('-s', '--sudo'): 
            sudo = True 
        elif opt in ('-r', '--release'): 
            release = arg 
        elif opt in ('--src',): 
            src_dir = arg 
        elif opt in ('--commit',): 
            commit = arg

    if release[0].isdigit():
        release = 'r' + release 
    release = 'origin/' + release

    if commit is not None: cmd = UPDATE_CMD % (src_dir, commit) 
    else: cmd = UPDATE_CMD % (src_dir, release)

    '''if sudo: 
        run('sudo %s' % cmd) 
    else: 
        run(cmd)'''
        
    print(cmd)
    
update(['False',SRC_DIR,RELEASE,None])
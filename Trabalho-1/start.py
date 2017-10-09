from subprocess import call

call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 0'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 1'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 2'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 3'])

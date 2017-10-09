from subprocess import call

call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 25000 0'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 25001 1'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 25002 2'])
call(['gnome-terminal' , '-e' ,'bash','--command','python rip.py 25003 3'])

import sys
import argparse
import os
from time import gmtime, strftime
import subprocess
from subprocess import Popen

CLI = argparse.ArgumentParser(description='Parses ITESMs calendar to Google Calendar')
CLI.add_argument(
    'mail',
    help = 'Student email'

)
CLI.add_argument(
    'pswd',
    help = 'Password used for ITESMs account'
)

args = CLI.parse_args()
command = 'scrapy crawl homepage -a mail="%s" -a pswd="%s" -o calendarEvents.json' % (args.mail, args.pswd)
print(command)
p = subprocess.Popen(command, shell=True)
p.wait()
if os.stat("calendarEvents.json").st_size == 0:
    print('Something went wrong. Double check credentials')
else:
    os.system('python calendarWriter.py')
    os.system('rm calendarEvents.json')

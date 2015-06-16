from termcolor import cprint
import json
import sys, os, traceback

def log_error(message):
    cprint(message, 'red')

def log_warn(message):
    cprint(message, 'yellow')

def log_info(message):
    cprint(message, 'cyan')

def log_success(message):
    cprint(message, 'green')

def log_json(list_dict):
    print json.dumps(list_dict, indent=2)

def log_dict(dict):
    for key, elem in dict.items():
        print '\t[{0}] {1}'.format(key, elem)

def log_debug(e, stacktrace=True):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    fname = os.path.split(exc_traceback.tb_frame.f_code.co_filename)[1]

    log_warn('[-] {0} {1} | {2}@{3}'.format(exc_type, e, fname, exc_traceback.tb_lineno))

    if stacktrace:
        traceback.print_exc()

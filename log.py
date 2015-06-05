import sys
import datetime
dest_file = sys.stdout
special_cases = {
    str: lambda o:o
}

def stringify(thing):
    for case in special_cases:
        if isinstance(thing, case):
            return special_cases[case](thing)
    else:
        return repr(thing)

def catargs(f):
    def res(*args):
        return f(' '.join(stringify(arg) for arg in args))
    return res

def wrap(color, name, tx):
    print('\x1b[30;4', color,
          datetime.datetime.now().strftime('m[%y-%m-%d %H:%M:%S]['),
          name, ']\x1b[0m\x1b[3', color, 'm ', tx, '\x1b[0m',
          sep='', file=dest_file)

@catargs
def note(tx):
    wrap('6', 'NOTE', tx)

@catargs
def warn(tx):
    wrap('3', 'WARNING', tx)

def err(tx):
    wrap('1', 'ERROR', tx)

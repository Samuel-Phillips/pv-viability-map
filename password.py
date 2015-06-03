import hashlib
import unicodedata
import sys
import getpass


def _hash(pwtext):
    """Perform the neccessary hashing on a normalized string."""
    return hashlib.sha512(_norm(pwtext)).digest()


def _norm(pwtext):
    """Normalize a password so they can compare right"""
    return unicodedata.normalize('NFKC', pwtext).encode('utf-8')


def check(pwtext):
    """Check if the given password string is, in fact, the correct one."""
    ps = _read()
    return _hash(pwtext) == ps  # potential race condition?


def set(pwtext):
    """Set the password"""
    _write(_hash(pwtext))


def _read():
    """Read the raw password hash from the file"""
    with open('password', mode='rb') as f:
        return f.read()


def _write(hashed):
    """Write the raw password hash to the file"""
    with open('password', mode='wb') as f:
        f.write(hashed)


def usage():
    print("Usage: python3 password.py ( set | check <password> )")
    print("Set or check the import form password")

if __name__ == '__main__':
    argv = sys.argv
    argc = len(argv)
    del argv[0]
    argc -= 1

    if argc > 0:
        if argv[0] == 'check':
            if argc == 2:
                sys.exit(0 if check(argv[1]) else 1)
            else:
                usage()
        elif argv[0] == 'set':
            if argc == 1:
                while True:
                    try:
                        pw1 = getpass.getpass(prompt="New Password: ")
                        pw2 = getpass.getpass(prompt="Retype New Password: ")
                        if pw1 == pw2:
                            set(pw1)
                            break
                        else:
                            print("They don't match")
                    except EOFError:
                        sys.exit(0)
            else:
                usage()
        else:
            usage()
    else:
        usage()

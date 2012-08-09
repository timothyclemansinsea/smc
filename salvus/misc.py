"""
Miscellaneous functions.
"""

import os

##########################################################################
# Connecting to HTTP url's.
##########################################################################
import socket, urllib, urllib2

def get(url, data=None, timeout=10):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        if data is not None:
            url = url + '?' + urllib.urlencode(data)
        return urllib2.urlopen(url).read()
    finally:
        socket.setdefaulttimeout(old_timeout)

def post(url, data=None, timeout=10):
    old_timeout = socket.getdefaulttimeout()
    socket.setdefaulttimeout(timeout)
    try:
        if data is None: data = {}
        data = urllib.urlencode(data)
        req = urllib2.Request(url, data)
        response = urllib2.urlopen(req)        
        return response.read()
    finally:
        socket.setdefaulttimeout(old_timeout)

##########################################################################
# Misc file/path management functions
##########################################################################
def all_files(path):   # TODO: delete if not used
    """
    Return a sorted list of the names of all files in the given path, and in
    all subdirectories.  Empty directories are ignored.

    INPUT:

    - ``path`` -- string

    EXAMPLES::

    We create 3 files: a, xyz.abc, and m/n/k/foo.  We also create a
    directory x/y/z, which is empty::

        >>> import tempfile
        >>> d = tempfile.mkdtemp()
        >>> o = open(os.path.join(d,'a'),'w')
        >>> o = open(os.path.join(d,'xyz.abc'),'w')
        >>> os.makedirs(os.path.join(d, 'x', 'y', 'z'))
        >>> os.makedirs(os.path.join(d, 'm', 'n', 'k'))
        >>> o = open(os.path.join(d,'m', 'n', 'k', 'foo'),'w')

    This all_files function returns a list of the 3 files, but
    completely ignores the empty directory::
    
        >>> all_files(d)       # ... = / on unix but \\ windows
        ['a', 'm...n...k...foo', 'xyz.abc']
        >>> import shutil; shutil.rmtree(d)       # clean up mess
    """
    all = []
    n = len(path)
    for root, dirs, files in os.walk(path):
        for fname in files:
            all.append(os.path.join(root[n+1:], fname))
    all.sort()
    return all


import tempfile

_temp_prefix = None
def is_temp_directory(path):  # TODO: delete if not used
    """
    Return True if the given path is likely to have been
    generated by the tempfile.mktemp function.

    EXAMPLES::

        >>> import tempfile
        >>> is_temp_directory(tempfile.mktemp())
        True
        >>> is_temp_directory(tempfile.mktemp() + '../..')
        False
    """
    global _temp_prefix
    if _temp_prefix is None:
        _temp_prefix = os.path.split(tempfile.mktemp())[0]
    path = os.path.split(os.path.abspath(path))[0]
    return os.path.samefile(_temp_prefix, path)


##########################################################################
# Misc process functions
##########################################################################

def is_running(pid):
    """Return True only if the process with given pid is running."""
    try:
        os.kill(pid,0)
        return True
    except:
        return False


##########################################################################
# Misc misc network stuff
##########################################################################

def local_ip_address():
    """
    Return the ip address of the local network interface that is used
    to communicate with the internet.
    """
    # See http://stackoverflow.com/questions/166506/finding-local-ip-addresses-using-pythons-stdlib
    # Obviously, this requires internet access.
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    return s.getsockname()[0]


##########################################################################
# Other
##########################################################################

import random, time, traceback

class call_until_succeed(object):
    """
    Decorator that makes it so that whenever a function is called, if
    any exception is raised, then the function is re-called with
    exactly the same arguments, after a delay.  The delay starts at
    mindelay seconds and exponentially (times 2) increases (with a
    slight random factor) until hitting maxdelay.  If it delays for a
    total of totaldelay and totaldelay is not None, then it gives up
    and re-raises the last exception.
    """
    def __init__(self, mindelay, maxdelay, totaldelay=None):
        self._mindelay = mindelay
        self._maxdelay = maxdelay
        self._totaldelay = totaldelay
        
    def __call__(self, f):
        def g(*args, **kwds):
            attempts = 0
            delay = (random.random() + 1)*self._mindelay
            totaldelay = 0
            while True:
                attempts += 1
                try:
                    return f(*args, **kwds)
                except:
                    if self._totaldelay and totaldelay >= self._totaldelay:
                        print("call_until_succeed: exception hit running %s; too long (>=%s)"%(f.__name__, self._totaldelay))
                        raise

                    # print stack trace and name of function
                    print("call_until_succeed: exception hit %s times in a row running %s; retrying in %s seconds"%(attempts, f.__name__, delay))
                    traceback.print_exc()
                    time.sleep(delay)
                    totaldelay += delay
                    delay = min(2*delay, self._maxdelay)
                    
        return g

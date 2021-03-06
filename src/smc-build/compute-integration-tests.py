#!/usr/bin/env python3
# Compute Image Integration Tests
# Goal of this testsuite is, to make sure that all relevant software, libraries and packages are installed.
# Each test either checks that it exists, maybe runs it, or even executes a short test, or display the version number.
import pytest
from textwrap import dedent
from subprocess import getstatusoutput, CalledProcessError

def run(cmd, expected_status = 0):
    status, output = getstatusoutput(cmd)
    if status == expected_status:
        return output
    else:
        raise CalledProcessError(cmd = cmd, returncode = status)

# binaries: each of them is:
# 1. name (also as string)
# 2. optional string to search in output
# 3. optional command line params (default: --version)
# 4. optional status code, because sometimes --version gives retcode of 1
BINARIES = [
    'git', 'latexmk', 'bash', 'gcc', 'clang', 'pdftk', 'julia', 'autopep8',
    ('hg', 'Mercurial'),
    ('cvs', 'Concurrent Versions System'),
    ('gp', 'GP/PARI CALCULATOR'),
    ('java', 'OpenJDK Runtime', '-version'),
    ('dot', 'dot - graphviz', '-V'),
    ('convert', 'ImageMagick'),
    ('ipython', '5'),
    ('ipython3', '5'),
    ('ssh', 'OpenSSH_7', '-V'),
    ('primesieve', 'primesieve 5', '--version', 1),
    ('plink', 'PLINK!', '', 1), # actually, p-link with a symlink to it
    ('polymake', 'polymake version 3'),
    ('pdflatex', 'pdfTeX 3.14'),
    ('python2', 'python 2.7'),
    ('python3', 'python 3'),
    ('xelatex', 'xetex'),
    ('axiom', 'AXIOMsys', '-h'),
    ('open-axiom', 'OpenAxiom 1'),
    ('giac', '1.2'),
    ('mpiexec', 'HYDRA'), # TODO there are several mpi versions, check that this one is the "good" one
    ('R', 'R version 3'),
    ('ocaml', 'version 4.', '-version'),
    ('clang', 'clang version 3'),
]

# python 2 libs
PY2 = [
    'numpy', 'scipy', 'matplotlib', 'pandas', 'statsmodels'
]

# python 3 libs
PY3 = [
    'numpy', 'scipy', 'matplotlib', 'pandas', # 'statsmodels'
]

# R libs
R = [
    'rstan',
]

# http://pytest.org/latest/parametrize.html#parametrized-test-functions
@pytest.mark.parametrize("bin", BINARIES)
def test_bin(bin):
    assert len(bin) > 0

# http://pytest.org/latest/parametrize.html#parametrized-test-functions
@pytest.mark.parametrize("bin", BINARIES)
def test_binaries(bin):
    if isinstance(bin, str):
        cmd = bin
        token = bin.lower()
        args = '--version'
        status = 0
    else:
        cmd = bin[0]
        token = bin[1] if len(bin) >= 2 else bin[0].lower()
        args = bin[2] if len(bin) >= 3 else '--version'
        status = bin[3] if len(bin) >= 4 else 0
    v = run('{cmd} {args}'.format(**locals()), status)
    assert token.lower() in v.lower()

@pytest.mark.parametrize("exe,libs", zip(['python2', 'python3'], [PY2, PY3]))
def test_python(exe, libs):
    CMD = dedent('''\
    {exe} -c "from __future__ import print_function
    import {lib}
    print('{exe} {lib}: ', end='')
    try:
        print({lib}.__version__)
    except:
        print({lib}.version())
    "''')
    for lib in libs:
        v = run(CMD.format(**locals()))
        print(v)
        assert lib.lower() in v.lower()

@pytest.mark.parametrize('lib', R)
def test_r(lib):
    CMD = '''echo "require('{lib}'); packageVersion('{lib}') " | R --vanilla --silent'''
    v = run(CMD.format(**locals()))
    print(v)
    assert lib.lower() in v.lower()


def test_doesnt_exist():
    with pytest.raises(CalledProcessError):
        'doesnt_exist' in run('doesnt_exist')

if __name__ == '__main__':
    #pytest.main()
    print('run $ py.test compute-integration-tests.py')

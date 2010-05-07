import os,sys

# the ryppl/tests/ subdirectory
here = os.path.dirname(os.path.abspath(__file__))

# Make the pip test facilities available
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(here)), 'tests'))

from path import *
from test_pip import *
from urllib import pathname2url
from cStringIO import StringIO

here = Path(here)

try:
    import distutils2
except ImportError:
    sys.path.insert(0, here.folder/'distutils2'/'src')
    import distutils2

from distutils2.metadata import DistributionMetadata as METADATA

def create_projects(env, **projects):
    index = env.scratch_path/'index'
    demand_dirs(index)
    repo = env.scratch_path/'repo'
    
    open(index/'index.html', 'w').write(
        '\n'.join(
            ['<html><head><title>Simple Index</title></head><body>']
            + [ '<a href=%r/>%s</a><br/>' % (p,p) for p in projects ]
            + ['</body></html>'])
        )
    
    paths = {}

    for p,metadata in projects.items():

        demand_dirs(index/p)

        paths[p] = repo/p
        demand_dirs(paths[p])

        env.run('git', 'init', cwd = paths[p])

        dot_ryppl = paths[p]/'.ryppl'

        if isinstance(metadata, basestring):
            m = METADATA()
            m.read_file(StringIO(metadata))
            metadata = m

        demand_dirs(dot_ryppl)
        metadata.write(dot_ryppl/'METADATA')

        env.run('git', 'add', Path('.ryppl')/'METADATA', cwd = paths[p])
        env.run('git', 'commit', '-m', 'initial checkin', cwd = paths[p])

        # Git bug?  This doesn't work!
        repo_url = pathname2url(paths[p])
        # repo_url = paths[p]

        open(index/p/'index.html', 'w').write(
            '<html><head><title>Links for %(p)s</title></head>'
            '<body>'
            '<h1>Links for %(p)s</h1>'
            '<a href="git+file://%(repo_url)s#egg=%(p)s">Git Repository</a><br/>'
            '</body></html>'
            % locals()
            )
        
    return index,paths

import unittest2

def reset():
    environ = os.environ.copy()
    environ['PATH'] = Path.pathsep.join([here.folder/'scripts', environ['PATH']])
    return reset_env(environ)

def ryppl(env, *args, **kw):
    if '--pdb' in sys.argv:
        return env.run('python', '-u', '-m', 'pdb', here.folder/'scripts'/'ryppl', *args, **kw)
    else:
        return env.run('ryppl', *args, **kw)

class Simple(unittest2.TestCase):

    def test_fetch(self):
        env = reset()
        index,project_paths = create_projects(
            env, my_proj=open(here.folder/'distutils2'/'src'/'distutils2'/'tests'/'PKG-INFO').read())
        ryppl(env, 'install', '--no-install', '-vvv', '-i', 'file://'+pathname2url(index), 'my_proj')


def test_suite():
    return unittest2.makeSuite(Simple)

if __name__ == '__main__':
    from distutils2.tests import run_unittest
    run_unittest(test_suite())

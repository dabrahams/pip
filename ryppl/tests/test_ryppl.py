import os,sys

# the directory containing all the tests
here = os.path.dirname(os.path.abspath(__file__))

# Make the pip test facilities available
sys.path.insert(0, os.path.join(os.path.dirname(here), 'tests'))

from path import *
from test_pip import *
from urllib import pathname2url

def create_projects(env, *projects):
    index = env.scratch_path/'index'
    demand_dirs(index)
    repo = env.scratch_path/'repo'
    
    open(index/'index.html', 'w').write(
        '\n'.join(
            ['<html><head><title>Simple Index</title></head><body>']
            + [ '<a href=%r/>%s</a><br/>' % (p,p) for p in projects ]
            + ['</body></html>'])
        )
    
    for p in projects:
        demand_dirs(index/p)

        repo_path = repo/p+'.git'
        demand_dirs(repo_path)
        env.run('git', 'init', '--bare', cwd = repo_path)

        repo_url = pathname2url(repo_path)

        open(index/p/'index.html', 'w').write(
            '<html><head><title>Links for %(p)s</title></head>'
            '<body>'
            '<h1>Links for %(p)s</h1>'
            '<a href="file://%(repo_url)s#egg=%(p)s">Git Repository</a><br/>'
            '</body></html>'
            % locals()
            )
        


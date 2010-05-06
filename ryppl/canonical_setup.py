import ryppl, sys, cStringIO
print '****** Canonical Ryppl setup.py file ******'
print 'command line:', sys.argv
print 'project directory =', repr(ryppl.project_directory)
print 'project name =', os.path.basename(ryppl.project_directory)

from distutils2.metadata import DistributionMetadata
import os
from setuptools import setup

metadata = DistributionMetadata(
    path=os.path.join(ryppl.project_directory, '.ryppl', 'METADATA'))

doc_dir = os.path.join(os.path.dirname(__file__), 'docs')

simple_kw_map = dict(summary='description', )
def metadata_to_setup_keywords(metadata):
    # There's probably a more programmatic way, but until then, I just
    # copied these keywords out of the distutils source

    class item_to_attribute(object):
        """
        because I hate seeing identifiers between quotes
        """
        def __init__(self, target):
            self.target = target

        def __getattr__(self, name):
            return self.target[name]

    m = item_to_attribute(metadata)
        
    return dict(
        # 'distclass': ???
        # 'script_name':???
        # 'script_args', ???
        # 'options', ???
        name = m.name,
        version = m.version,
        author = m.author,
        author_email = m.author_email,
        maintainer = m.maintainer,
        maintainer_email = m.maintainer_email,
        url = m.project_url,
        description = m.summary,
        long_description = m.description,
        keywords = ' '.join(m.keywords),
        platforms = m.platform,
        classifiers = m.classifier, 
        download_url = m.download_url,
        # We'll need to translate requirements to setuptools format
        # requires = m.requires_dist or m.requires,
        provides = m.provides_dist or m.provides,
        obsoletes = m.obsoletes_dist or m.obsoletes,
        )

setup( **metadata_to_setup_keywords(metadata) )

import ryppl, sys
print '****** Canonical Ryppl setup.py file ******'
print 'command line:', sys.argv
print 'project directory =', repr(ryppl.project_directory)
print 'project name =', os.path.basename(ryppl.project_directory)

from setuptools import setup
import os

pkg_dir = os.path.join(ryppl.project_directory,'boost_python')
if not os.path.isdir(pkg_dir):
    os.mkdir(pkg_dir)
    
version = "0.9.0"

doc_dir = os.path.join(os.path.dirname(__file__), 'docs')
index_filename = os.path.join(doc_dir, 'index.txt')

long_description = """\
The main website for ryppl is `ryppl.org <http://ryppl.org>`_.  
"""
try:
    long_description = long_description + open(index_filename).read().split('split here', 1)[1]
except:
    pass

setup(name=os.path.basename(ryppl.project_directory),
      version=version,
      description="A ryppl package",
      long_description=long_description,
      classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Topic :: Software Development :: Build Tools',
      ],
      keywords='easy_install distutils setuptools egg virtualenv pip package',
      author='The Ryppl Project',
      author_email='ryppl-dev@groups.google.com',
      url='http://ryppl.org',
      license='MIT',
      install_requires='boost-type_traits>0.7.3dev',
      dependency_links=['http://dabrahams.github.com/ryppl-test-index']
      )
      

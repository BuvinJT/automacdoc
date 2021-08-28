import setuptools

# get __version__ value and readme text
exec( open('pymkdocs/_version.py').read() ) 
with open( "README.md", "r" ) as f: readme = f.read()

setuptools.setup(
     name='pymkdocs',
     version=__version__,  # @UndefinedVariable
     entry_points={"console_scripts": ["pymkdocs = pymkdocs.main:main"]},
     author="BuvinJ",
     author_email="buvintech@gmail.com",
     description=("Documentation generator for Python, using markdown and MkDocs."),
     long_description=readme,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     install_requires=['mkdocs', 'mkdocs-material', 'pymdown-extensions'],
     classifiers=[
         "Development Status :: 3 - Alpha",         
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
         "Intended Audience :: Developers",
         "Topic :: Documentation"
     ],
 )
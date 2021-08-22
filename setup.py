import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
     name='pymkdocs',
     version='0.4',
     entry_points={"console_scripts": ["pymkdocs = pymkdocs.main:main"]},
     author="BuvinJ",
     author_email="buvintech@gmail.com",
     description=("Documentation generator for Python, using markdown and MkDocs."),
     long_description=long_description,
     long_description_content_type="text/markdown",
     packages=setuptools.find_packages(),
     install_requires=['mkdocs', 'mkdocs-material', 'pymdown-extensions'],
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )
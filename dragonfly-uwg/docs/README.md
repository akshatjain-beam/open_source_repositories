
## Usage
For generating the documents locally use commands below from the root folder. 

commit hash - 61fcc166ef7d9a7e0450aba9ad87d1f8b696e593 

```shell
# install dependencies
pip install Sphinx sphinxcontrib-fulltoc sphinx_bootstrap_theme

# generate rst files for modules
sphinx-apidoc -f -e -d 4 -o ./docs ./dragonfly_uwg
# build the documentation under _build/docs folder
sphinx-build -b html ./docs ./docs/_build/docs
```

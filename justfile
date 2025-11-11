# CLI helpers.

# Help
help:
    @just -l

# Run all pre-commit checks
pre-commit:
   pre-commit run --all-files

# Package repository as tar for easy distribution
tar-source: package-deps
	rm -rf tar-src/
	mkdir tar-src/
	git-archive-all --prefix jsonid/ tar-src/jsonid-v0.0.0.tar.gz

# Upgrade dependencies for packaging
package-deps:
	python3 -m pip install -U twine wheel build git-archive-all

# Package the source code
package-source: package-deps clean
	python -m build .

# Check the distribution is valid
package-check: clean package-source
	twine check dist/*

# Upload package to test.pypi
package-upload-test: clean package-deps package-check
	twine upload dist/* --repository-url https://test.pypi.org/legacy/ --verbose

# Upload package to pypi
package-upload: clean package-deps package-check
	twine upload dist/* --repository-url https://upload.pypi.org/legacy/ --verbose

# Package
package: package-upload

# Generate documentation
docs: && htm
   rm -rf docs/*
   pdoc3 --force --html -o docs src/
   mv -f docs/src/* docs/.
   cp static/images/JSON_logo-crockford.png docs/favicon.ico
   mkdir docs/registry
   rm -rf docs/src

# Export registry as HTM
htm:
   rm -rf docs/registry/*
   python jsonid.py --htm > docs/registry/index.htm
   cp static/images/JSON_logo-crockford.png docs/registry/favicon.ico

# Serve the documentation
serve-docs:
   python -m http.server --directory docs/

# Serve the registry
serve-registry:
   python -m http.server --directory docs/registry/

# Upgrade project dependencies
upgrade:
	pip-upgrade

# Clean the package directory
clean:
	rm -rf src/*.egg-info/
	rm -rf build/
	rm -rf dist/
	rm -rf tar-src/

# Check the registry entries are correct.
check:
   python jsonid.py --check

# Check the registry entries are correct (DEBUG).
check-debug:
   python jsonid.py --check --debug

# Hexdump a file in Python hex format
@hexdump file:
   hexdump -v -e '"\\\x" 1/1 "%02x"' {{file}}

# Hexdump bytes only.
@hexdump-plain file:
    hexdump -ve '1/1 "%.2x"' {{file}}

# code coverage
coverage:
 python -m tox -e coverage

# lookup registry example (core)
lookup-core-ex:
 python jsonid.py core JSON

# lookup registry example (doctype)
lookup-ref-ex:
 python jsonid.py lookup jrid:0055

# lookup core
@lookup-core core:
 python jsonid.py core {{core}}

# lookup ref
@lookup-ref ref:
 python jsonid.py lookup {{ref}}

# export as PRONOM
pronom:
 python jsonid.py --pronom --debug

# move pronom to .droid folder
pronom-to-droid:
 ~/.droid6/clean.sh
 rm -f ~/.droid6/signature_files/jsonid_pronom.xml
 cp jsonid_pronom.xml ~/.droid6/signature_files/

dir := `pwd`

# load pronom to siegfried via roy
roy:
 @echo {{dir}}
 roy build --noreports -extend {{dir}}/jsonid_pronom.xml

# droid-cli
droid-cli path: pronom-to-droid
 java -jar ~/dp/droid/droid-binary-6.8.0-bin/droid-command-line-6.8.0.jar -s 1
 java -jar ~/dp/droid/droid-binary-6.8.0-bin/droid-command-line-6.8.0.jar -ri  {{path}}

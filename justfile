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
docs:
   rm -rf docs/*
   pdoc3 --force --html -o docs src/
   mv -f docs/src/* docs/.
   rm -rf docs/src

# Serve the documentation
serve-docs:
   python -m http.server --directory docs/

# Upgrade project dependencies
upgrade:
	pip-upgrade

# Clean the package directory
clean:
	rm -rf src/*.egg-info/
	rm -rf build/
	rm -rf dist/
	rm -rf tar-src/

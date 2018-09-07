# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXAPIDOC  = sphinx-apidoc
SPHINXPROJ    = strpipe
SOURCEDIR     = source
BUILDDIR      = build
CODEDIR       = $(realpath ../$(SPHINXPROJ))

# Default is to regenerate API stubs and make HTML documentation
all:
	@echo ***Regenerating API stubs and building html files***
	make apidoc
	make html

apidoc:
	@echo ***Regenerating API stubs for code in $(CODEDIR)***
	rm -r $(SOURCEDIR)/reference || true
	$(SPHINXAPIDOC) -f -o $(SOURCEDIR)/reference $(CODEDIR) $(CODEDIR)/test* $(CODEDIR)/**/test/* $(CODEDIR)/**/tests/*

# Put it first so that "make" without argument is like "make help".
help:
	@echo ***targets from sphinx-build***
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
	@echo ***other custom targets***
	@echo -e '  apidocs\tbuild apidoc sources'

.PHONY: help Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $@ "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

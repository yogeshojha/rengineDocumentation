PY      ?= .venv/bin/python
MKDOCS  ?= .venv/bin/mkdocs
ADDR    ?= 127.0.0.1:8008
RENGINE ?= ../rengine

export NO_MKDOCS_2_WARNING = true

.PHONY: help snapshot gen serve build check lint links clean

help:
	@echo "snapshot  refresh data/repo.json from $(RENGINE)"
	@echo "gen       write the generated reference pages from data/"
	@echo "serve     serve the site on http://$(ADDR)"
	@echo "build     build the site into site/ with --strict"
	@echo "check     gen, build, copy lint and link check"

snapshot:
	python3 scripts/snapshot_repo.py --repo $(RENGINE)

gen:
	python3 scripts/gen_all.py

serve: gen
	$(MKDOCS) serve -a $(ADDR)

build: gen
	$(MKDOCS) build --strict

lint:
	python3 scripts/lint_copy.py

links:
	python3 scripts/check_site.py

check: build lint links

clean:
	rm -rf site

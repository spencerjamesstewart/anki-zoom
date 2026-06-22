# anki-zoom — build & dev helpers
#
# Anki imports an add-on by its folder name, which must be a valid Python
# identifier — hence "anki_zoom" (underscore), not the repo's "anki-zoom".
#
# On Linux, override the add-ons dir:
#   make link ADDONS_DIR=~/.local/share/Anki2/addons21

ADDONS_DIR ?= $(HOME)/Library/Application Support/Anki2/addons21
PACKAGE    := anki_zoom
SRC        := __init__.py config.json config.md manifest.json
ARTIFACT   := $(PACKAGE).ankiaddon

.PHONY: build link unlink clean

# Package a distributable .ankiaddon (a plain zip with the files at its root).
build: $(ARTIFACT)

$(ARTIFACT): $(SRC)
	rm -f $(ARTIFACT)
	zip -j $(ARTIFACT) $(SRC)

# Symlink this repo into Anki for live development. Restart Anki after linking.
link:
	ln -snf "$(CURDIR)" "$(ADDONS_DIR)/$(PACKAGE)"
	@echo "Linked -> $(ADDONS_DIR)/$(PACKAGE)  (restart Anki)"

unlink:
	rm -f "$(ADDONS_DIR)/$(PACKAGE)"

clean:
	rm -f $(ARTIFACT)

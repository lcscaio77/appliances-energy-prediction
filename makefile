# Variables
PYTHON := python3
PIP := pip
VENV_DIR := venv
REQ_FILE := requirements.txt
ACTIVATE := $(VENV_DIR)/bin/activate

# Détection du système d'exploitation
ifeq ($(OS),Windows_NT)
	PYTHON := python
	PIP := pip
	ACTIVATE := $(VENV_DIR)\\Scripts\\activate
endif

# Cible principale : installation du venv et des dépendances
default: setup activate

# Création de l'environnement virtuel
$(VENV_DIR):
	@echo "Création de l'environnement virtuel dans $(VENV_DIR)"
	$(PYTHON) -m venv $(VENV_DIR)

# Installation des dépendances
install: $(VENV_DIR)
	@echo "Installation des dépendances depuis $(REQ_FILE)"
	$(VENV_DIR)/bin/$(PIP) install -r $(REQ_FILE) || $(VENV_DIR)\\Scripts\\$(PIP) install -r $(REQ_FILE)

# Activation de l'environnement virtuel
activate: $(VENV_DIR)
	@echo "Pour activer le venv, exécutez :"
ifeq ($(OS),Windows_NT)
	@echo "    .\\$(VENV_DIR)\\Scripts\\activate"
else
	@echo "    source $(ACTIVATE)"
endif

# Configuration complète : venv + dépendances
setup: $(VENV_DIR) install

# Nettoyage
clean:
	@echo "Suppression de l'environnement virtuel $(VENV_DIR)"
	@rm -rf $(VENV_DIR)

.PHONY: default setup install activate clean

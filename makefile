# Détection de l'OS
UNAME_S := $(shell uname -s)

# Variables
PYTHON=python3

ifneq (,$(filter $(UNAME_S),Darwin Linux))
    ACTIVATE_SCRIPT=venv/bin/activate
else ifneq (,$(findstring CYGWIN $(UNAME_S) MINGW,$(UNAME_S)))
    ACTIVATE_SCRIPT=venv/Scripts/activate
else
    $(error "OS non supporté pour ce Makefile")
endif

.PHONY: all setup activate clean

# Règle principale
all: setup
	@echo "Configuration terminée ! Pour activer l'environnement virtuel, tapez :\nsource $(ACTIVATE_SCRIPT)"

# Création et configuration de l'environnement virtuel
setup:
	@echo "Détection de l'OS : $(UNAME_S)"
	$(PYTHON) -m venv venv
	@echo "Environnement virtuel créé."
	@echo "Mise à jour de pip..."
	venv/bin/pip install --upgrade pip
	@echo "Installation des dépendances..."
	venv/bin/pip install -r requirements.txt
	@echo "Installation des dépendances terminée."

# Activation de l'environnement virtuel
activate:
	@echo "Pour activer l'environnement virtuel, tapez :\nsource $(ACTIVATE_SCRIPT)"

# Nettoyage
clean:
	@echo "Suppression de l'environnement virtuel..."
	rm -rf venv
	@echo "Nettoyage terminé."

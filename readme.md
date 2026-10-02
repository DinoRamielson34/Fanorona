# Fanorona Telo (Fanorina) - Application Tkinter en Python

Ce projet est une implémentation en Python de l'un des jeux traditionnels malgaches les plus célèbres : le **Fanorona Telo** (ou *Fanorina*). Développé avec l'interface graphique **Tkinter**, le programme intègre un moteur de jeu complet, plusieurs modes (Humain vs Humain, Humain vs IA, IA vs IA) et une intelligence artificielle basée sur l'algorithme **Minimax** avec élagage Alpha-Bêta.

---

## 📋 Table des matières

1. [Règles du Jeu](#-règles-du-jeu)
2. [Fonctionnalités Principales](#-fonctionnalités-principales)
3. [Architecture du Code](#-architecture-du-code)
4. [Algorithme de l'Intelligence Artificielle](#-algorithme-de-lintelligence-artificielle)
5. [Installation et Exécution](#-installation-et-exécution)

---

## 🎮 Règles du Jeu

Le Fanorona Telo se joue sur une grille de $3 \times 3$ intersections reliées par des lignes horizontales, verticales et diagonales.

### Phases de jeu :
1. **Phase de Placement** :
   - Chaque joueur pose tour à tour **3 pions** sur les intersections vides du plateau.
   - **Règle d'ouverture** : Il est interdit de placer un pion au centre $(1, 1)$ lors du tout premier tour de la partie.
   - **Condition de position** : Un pion ne peut être placé que s'il dispose d'au moins un côté libre/adjacent.
2. **Phase de Déplacement** :
   - Une fois tous les pions posés, les joueurs déplacent à tour de rôle un de leurs pions vers une intersection adjacente vide.
3. **Condition de Victoire** :
   - Le premier joueur qui aligne ses 3 pions (en ligne, colonne ou diagonale) remporte la partie.

---

## ✨ Fonctionnalités Principales

- **Modes de Jeu Sélectionnables** :
  - `Humain vs IA` (par défaut) : Jouez contre l'ordinateur.
  - `Humain vs Humain` : Deux joueurs s'affrontent sur le même écran.
  - `IA vs IA` : Observez deux algorithmes s'affronter au coup par coup.
- **Règles Spéciales & Variantes** :
  - **Point Noir Bloquant** : Un bouton permet de placer un obstacle neutre ("N") sur le plateau pour pimenter la stratégie.
- **Gestion Visuelle** :
  - Dessin dynamique du plateau via le composant `Canvas`.
  - Surlignage de la pièce sélectionnée en jaune.
  - Messages d'erreur contextuels et bannière de fin de partie.

---

## 🏗️ Architecture du Code

Le script repose sur la classe principale `Fanorina` :

| Méthode / Module | Description |
| :--- | :--- |
| `__init__` & `create_interface` | Initialise le canvas, les points d'intersection et les boutons de contrôle Tkinter. |
| `recommencer` | Réinitialise toutes les variables d'état du plateau et remet la partie à zéro. |
| `clic(event)` | Intercepte les clics de la souris pour la sélection/placement des pions par un joueur humain. |
| `is_valid_move` & `has_adjacent_empty_side` | Vérifient la validité des coups selon la géométrie et les contraintes du jeu. |
| `redessiner_plateau` | Efface et redessine l'intégralité des lignes, intersections et pions (`V` pour Vert, `R` pour Rouge, `N` pour Noir). |
| `check_victory_on_board` | Parcourt l'ensemble des 8 alignements gagnants possibles (3 lignes, 3 colonnes, 2 diagonales). |

---

## 🧠 Algorithme de l'Intelligence Artificielle

L'IA repose sur la méthode `ia_joue` couplée à un algorithme **Minimax** (`minimax` et `evaluate_board`) :

1. **Profondeur d'exploration** : Fixée à 3 coups d'anticipation pour garantir un temps de réponse instantané.
2. **Élagage Alpha-Bêta** : Optimise la recherche dans l'arbre des possibilités en coupant les branches inutiles.
3. **Fonction d'Évaluation** (`evaluate_board`) :
   - Attribue un score positif pour les alignements partiels de l'IA et négatif pour ceux de l'adversaire.
   - PONDÉRATION : Bonus stratégique accordé au joueur qui contrôle la case centrale $(1, 1)$.

---

## 🚀 Installation et Exécution

### Prérequis
- **Python 3.x** installé sur votre machine.
- Le module **Tkinter** (généralement inclus par défaut avec Python).

### Lancer le jeu
1. Copiez le code Python dans un fichier nommé `fanorona.py`.
2. Ouvrez votre terminal et exécutez la commande :

```bash
python fanorona.py
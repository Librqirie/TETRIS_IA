# Tetris à deux joueurs (Humain vs IA)

Un jeu de Tetris avec deux joueurs - un humain et une IA - développé en Python avec Tkinter. Le jeu comprend des règles spéciales pour une expérience plus amusante.


## Description

Ce projet est un jeu de Tetris à deux joueurs où vous jouez contre une IA. Chaque joueur dispose de sa propre grille, et le but est de réaliser le meilleur score possible en complétant des lignes. Le jeu comprend plusieurs règles originales qui rendent l'expérience plus intéressante.

## Fonctionnalités

- **Deux grilles de jeu** : une pour le joueur humain et une pour l'IA
- **Système de score** avec des bonus pour les lignes multiples
- **Règles spéciales** :
  - **Cadeau surprise** : Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une pièce facile
  - **Pause douceur** : Tous les 1000 points, les pièces tombent 20% plus lentement pendant 10 secondes
  - **Pièce rigolote** : Tous les 3000 points, une pièce spéciale (cœur ou étoile) apparaît et vaut 100 points bonus
  - **Arc-en-ciel** : Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes

## Prérequis

- Python 3.6 ou supérieur
- Tkinter (généralement inclus avec Python)

## Installation

1. Clonez ce dépôt :
   ```bash
   git clone https://github.com/Librqirie/TETRIS_IA.git
   cd tetris-ia
   ```

2. Aucune dépendance supplémentaire n'est nécessaire car le projet utilise uniquement la bibliothèque standard Python.

## Comment lancer le jeu

Exécutez simplement le fichier principal :

```bash
python main.py
```

ou

```bash
py main.py
```

## Contrôles

### Joueur humain
- **Flèche gauche** : Déplacer la pièce vers la gauche
- **Flèche droite** : Déplacer la pièce vers la droite
- **Flèche bas** : Accélérer la descente de la pièce
- **Flèche haut** : Faire pivoter la pièce
- **Espace** : Faire tomber la pièce instantanément
- **P** : Mettre le jeu en pause / Reprendre
- **R** : Redémarrer le jeu

### IA
L'IA joue automatiquement en évaluant les meilleures positions possibles pour chaque pièce.

## Système de score

- **50 points** par ligne complétée
- **Bonus** :
  - **100 points** supplémentaires pour 2 lignes d'un coup (total: 200 points)
  - **200 points** supplémentaires pour 3 lignes d'un coup (total: 350 points)
  - **300 points** supplémentaires pour 4 lignes d'un coup (total: 500 points)
- **100 points** bonus pour chaque pièce spéciale bien placée

## Structure du projet

Le projet est contenu dans un seul fichier main.py qui inclut les classes suivantes :
- `Piece` : Représente une pièce de Tetris
- `Board` : Représente le plateau de jeu
- `HumanPlayer` : Gère les actions du joueur humain
- `AIPlayer` : Implémente la logique de l'IA
- `TetrisGame` : Classe principale qui gère le jeu et l'interface utilisateur

## Développement

Ce projet a été développé à l'aide de GitHub Copilot dans le cadre d'un cours sur l'IA générative et la génération de code. Tous les prompts utilisés pour générer le code sont documentés dans le fichier PROMPTS.md.
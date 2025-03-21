# Prompts utilisés pour générer le projet

## Prompt 1 (GPT-4o) :

fais-en un prompt :
Je dois créer un projet dans le cadre d'un cours sur l'IA générative et son utilisation pour la génération de code. Je vais te donner le sujet du projet et j'aimerai que tu écrives un prompt détaillé et bien structuré à destination de Claude afin qu'il me génère le projet dans vscode via Copilot. Tu dois me fournir un prompt sous forme de texte que je peux facilement copier/coller.
Voici le sujet du projet : "Projet : Tetris à deux joueurs (Humain vs IA)
Vous devez coder un Tetris en Python avec Tkinter, avec deux joueurs : un humain et
une IA. Il faut une grille pour chaque joueur et un tableau des scores. Voici les détails avec des règles originales :
Fonctionnalités principales
Deux grilles
Une pour le joueur humain, une pour l'IA, côte à côte.
Contrôles
Humain : flèches du clavier (gauche, droite, bas, haut pour tourner).
IA : joue automatiquement avec une logique simple (ex. : placer les pièces au mieux sans trop réfléchir).
Tableau des scores
Points :
50 par ligne.
Bonus : 100 pour 2 lignes, 200 pour 3 lignes, 300 pour un Tetris (4 lignes).
Affiche les scores en direct pour les deux joueurs.
Règles fun
1. Cadeau surprise
Quand un joueur complète 2 lignes d'un coup, l'adversaire reçoit une "pièce facile" (ex. : un carré ou une ligne droite) pour l'aider un peu.
2. Pause douceur
Tous les 1 000 points, les pièces tombent 20 % plus lentement pendant 10 secondes pour les deux joueurs – un petit répit pour souffler !
3. Pièce rigolote
Tous les 3 000 points, une pièce spéciale apparaît (ex. : une pièce en forme de cœur ou d'étoile), qui vaut 100 points bonus si elle est bien placée.
4. Arc-en-ciel
Toutes les 2 minutes, les pièces changent de couleur pendant 20 secondes pour rendre le jeu plus joli (pas de piège, juste du fun visuel).
Rendu du projet
Le projet complet doit être mis sur GitHub en dépôt public.
Le dépôt doit contenir :
Tout le code source du jeu
Un fichier PROMPTS.md documentant la liste des prompts utilisés pour réaliser le projet
Un fichier README.md qui contient la procédure pour lancer le projet
Critères d'évaluation (20 points)
Qualité des prompts (10 points)
Pertinence et efficacité des prompts utilisés (4 points)
Créativité et originalité dans l'approche (3 points)
Documentation complète de tous les prompts dans un fichier PROMPTS.md (3 points)
Fonctionnalités du jeu (7 points)
Implémentation des deux grilles de jeu (1.5 points)
Contrôles du joueur humain et IA fonctionnels (1.5 points)
Système de score complet (1 point)
Implémentation des règles fun (3 points)
Documentation et utilisabilité (3 points)
README.md détaillé avec instructions claires pour lancer le projet (1.5 points)
Structure du code lisible et bien organisée (0.5 point)
Absence de bugs majeurs (1 point)"


### Prompt 2 (Claude 3.7 Sonnet Thinking / Github Copilot) :
 
### **Tetris à deux joueurs (Humain vs IA) en Python avec Tkinter**  

#### **Contexte**  
Je dois réaliser un projet dans le cadre d'un cours sur l'IA générative et son utilisation pour la génération de code. Ce projet consiste à coder un jeu de **Tetris à deux joueurs (Humain vs IA)** en **Python avec Tkinter**. Le jeu doit inclure une grille pour le joueur humain, une grille pour l'IA, un tableau des scores et plusieurs règles originales pour rendre l'expérience plus amusante.  

Ton objectif est de **générer un projet structuré et fonctionnel en un fichier main.py** en respectant les contraintes et fonctionnalités décrites ci-dessous.  

---

#### **Objectifs du projet**  
Créer un **jeu de Tetris en Python avec Tkinter**, en respectant les exigences suivantes :  

- **Deux grilles de jeu** : une pour le joueur humain et une pour l'IA, affichées côte à côte.  
- **Contrôles** :  
  - **Joueur humain** : flèches du clavier (gauche, droite, bas, haut pour tourner).  
  - **IA** : joue automatiquement avec une **logique simple** (placer les pièces au mieux sans trop réfléchir).  
- **Tableau des scores** :  
  - 50 points par ligne complétée.  
  - Bonus :  
    - 100 points pour 2 lignes d'un coup.  
    - 200 points pour 3 lignes.  
    - 300 points pour un Tetris (4 lignes).  
  - Affichage des scores en direct pour les deux joueurs.  
- **Règles fun à implémenter** :  
  1. **Cadeau surprise** : Lorsqu'un joueur complète **2 lignes d'un coup**, l'adversaire reçoit une **pièce facile** (ex. : un carré ou une ligne droite).  
  2. **Pause douceur** : Tous les **1 000 points**, les pièces tombent **20 % plus lentement** pendant **10 secondes** pour les deux joueurs.  
  3. **Pièce rigolote** : Tous les **3 000 points**, une **pièce spéciale** (ex. : cœur ou étoile) apparaît et vaut **100 points bonus** si elle est bien placée.  
  4. **Arc-en-ciel** : Toutes les **2 minutes**, les pièces **changent de couleur** pendant **20 secondes** (effet purement visuel).   

---

#### **Critères de qualité à respecter**  
- **Code clair et structuré** : utiliser des classes et des fonctions bien organisées.  
- **Aucune dépendance inutile** : le jeu doit être exécutable avec une installation minimale.  
- **Lisibilité et documentation** : ajouter des commentaires et documenter les fichiers principaux.  
- **Respect des règles et fonctionnalités demandées**.  

---

### **Sortie attendue**  
À la fin, Copilot doit générer **un projet fonctionnel, bien structuré et exécutable** en lançant :  

py main.py

Tout doit être **mis sur un dépôt GitHub public**, avec une documentation claire pour lancer le projet.


### Prompt 3 (Claude 3.7 Sonnet Thinking / Github Copilot) :

règle l'affichage des grilles, c'est coupé en bas
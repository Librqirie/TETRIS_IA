import tkinter as tk
from tkinter import messagebox
import random
import time
import threading
import copy
from enum import Enum
import math

# Définition des constantes
BOARD_WIDTH = 10
BOARD_HEIGHT = 20
BLOCK_SIZE = 30
AI_THINKING_TIME = 0.5  # Temps que l'IA prend pour "réfléchir" (secondes)
SPECIAL_PIECE_BONUS = 100
RAINBOW_INTERVAL = 120  # 2 minutes en secondes
RAINBOW_DURATION = 20  # 20 secondes

# Couleurs pour les pièces
COLORS = {
    'I': '#00FFFF',  # Cyan
    'J': '#0000FF',  # Bleu
    'L': '#FF8000',  # Orange
    'O': '#FFFF00',  # Jaune
    'S': '#00FF00',  # Vert
    'T': '#8000FF',  # Violet
    'Z': '#FF0000',  # Rouge
    'HEART': '#FF69B4',  # Rose pour la pièce spéciale cœur
    'STAR': '#FFD700',  # Or pour la pièce spéciale étoile
    'EMPTY': '#000000',  # Noir pour les cases vides
    'BORDER': '#333333'  # Gris pour les bordures
}

# Définition des formes de pièces
SHAPES = {
    'I': [
        [(0, 0), (0, 1), (0, 2), (0, 3)],
        [(0, 0), (1, 0), (2, 0), (3, 0)]
    ],
    'J': [
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (0, 1), (1, 0), (2, 0)],
        [(0, 0), (0, 1), (0, 2), (1, 2)],
        [(0, 1), (1, 1), (2, 0), (2, 1)]
    ],
    'L': [
        [(0, 0), (0, 1), (0, 2), (1, 0)],
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (1, 2), (0, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1)]
    ],
    'O': [
        [(0, 0), (0, 1), (1, 0), (1, 1)]
    ],
    'S': [
        [(0, 1), (0, 2), (1, 0), (1, 1)],
        [(0, 0), (1, 0), (1, 1), (2, 1)]
    ],
    'T': [
        [(0, 1), (1, 0), (1, 1), (1, 2)],
        [(0, 0), (1, 0), (2, 0), (1, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 1)],
        [(1, 0), (0, 1), (1, 1), (2, 1)]
    ],
    'Z': [
        [(0, 0), (0, 1), (1, 1), (1, 2)],
        [(0, 1), (1, 0), (1, 1), (2, 0)]
    ],
    'HEART': [
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)]  # Forme de coeur simplifiée
    ],
    'STAR': [
        [(0, 1), (1, 0), (1, 1), (1, 2), (2, 0), (2, 2)]  # Forme d'étoile simplifiée
    ]
}

# Classe pour représenter une pièce de Tetris
class Piece:
    def __init__(self, shape_name=None):
        if shape_name is None:
            # Pièce aléatoire normale
            self.shape_name = random.choice(['I', 'J', 'L', 'O', 'S', 'T', 'Z'])
        else:
            self.shape_name = shape_name
            
        self.rotation = 0
        self.x = BOARD_WIDTH // 2 - 1
        self.y = 0
        self.shapes = SHAPES[self.shape_name]
        self.color = COLORS[self.shape_name]
        
    def get_blocks(self):
        shape = self.shapes[self.rotation % len(self.shapes)]
        return [(self.x + x, self.y + y) for x, y in shape]
    
    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.shapes)
    
    def move(self, dx, dy):
        self.x += dx
        self.y += dy
    
    def is_special(self):
        return self.shape_name in ['HEART', 'STAR']

# Classe pour représenter le plateau de jeu
class Board:
    def __init__(self):
        self.grid = [[None for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
        self.current_piece = None
        self.next_piece = None
        self.score = 0
        self.level = 1
        self.fall_speed = 1.0  # Vitesse de chute initiale
        self.speed_modifier = 1.0  # Modificateur pour ralentir/accélérer
        self.speed_modifier_timer = None
        self.rainbow_mode = False
        self.game_over = False
        self.special_piece_types = ['HEART', 'STAR']
        self.easy_piece_types = ['O', 'I']
        self.special_piece_counter = 0
        
    def new_piece(self, specific_piece=None):
        if specific_piece:
            self.current_piece = Piece(specific_piece)
        elif self.next_piece:
            self.current_piece = self.next_piece
            # Vérification pour ajouter une pièce spéciale
            if self.special_piece_counter >= 3000:
                self.special_piece_counter = 0
                self.next_piece = Piece(random.choice(self.special_piece_types))
            else:
                self.next_piece = Piece()
        else:
            # Au premier tour seulement
            self.current_piece = Piece()
            self.next_piece = Piece()
        
        # Vérifier si la pièce peut être placée
        if not self.is_valid_position():
            self.game_over = True
            return False
        
        return True
    
    def is_valid_position(self, piece=None, x_offset=0, y_offset=0):
        if piece is None:
            piece = self.current_piece
        
        # Récupérer les blocs de la pièce
        blocks = piece.get_blocks()
        
        for x, y in blocks:
            # Ajout des offsets
            test_x = x + x_offset
            test_y = y + y_offset
            
            # Vérifier si la position est valide
            if (test_x < 0 or test_x >= BOARD_WIDTH or 
                test_y < 0 or test_y >= BOARD_HEIGHT or
                (test_y >= 0 and self.grid[test_y][test_x] is not None)):
                return False
                
        return True
    
    def try_rotate(self):
        if not self.current_piece:
            return False
            
        # Sauvegarde de la rotation actuelle
        original_rotation = self.current_piece.rotation
        
        # Essayer de tourner
        self.current_piece.rotate()
        
        # Vérifier si la rotation est valide
        if not self.is_valid_position():
            # Si la rotation n'est pas valide, revenir à l'état précédent
            self.current_piece.rotation = original_rotation
            return False
            
        return True
    
    def try_move(self, dx, dy):
        if not self.current_piece:
            return False
            
        if self.is_valid_position(x_offset=dx, y_offset=dy):
            self.current_piece.move(dx, dy)
            return True
            
        return False
    
    def lock_piece(self):
        if not self.current_piece:
            return 0
            
        blocks = self.current_piece.get_blocks()
        is_special = self.current_piece.is_special()
        
        # Ajouter la pièce à la grille
        for x, y in blocks:
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                self.grid[y][x] = self.current_piece.color
        
        # Vérifier les lignes complètes
        lines_cleared = self.clear_lines()
        
        # Mettre à jour le score
        points = self.calculate_score(lines_cleared)
        
        # Ajouter des points bonus pour une pièce spéciale
        if is_special:
            points += SPECIAL_PIECE_BONUS
        
        self.score += points
        self.special_piece_counter += points
        
        # Mettre à jour la vitesse en fonction du niveau
        self.level = max(1, self.score // 1000 + 1)
        self.update_fall_speed()
        
        return lines_cleared
    
    def calculate_score(self, lines_cleared):
        if lines_cleared == 0:
            return 0
        elif lines_cleared == 1:
            return 50
        elif lines_cleared == 2:
            return 150  # 50 + 100 bonus
        elif lines_cleared == 3:
            return 250  # 50*3 + 100 bonus
        elif lines_cleared == 4:
            return 500  # 50*4 + 300 bonus
        return 0
    
    def clear_lines(self):
        lines_to_clear = []
        
        # Trouver les lignes complètes
        for y in range(BOARD_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(BOARD_WIDTH)):
                lines_to_clear.append(y)
        
        # Effacer les lignes et faire descendre les blocs
        for y in lines_to_clear:
            # Déplacer toutes les lignes au-dessus vers le bas
            for y2 in range(y, 0, -1):
                for x in range(BOARD_WIDTH):
                    self.grid[y2][x] = self.grid[y2-1][x]
            
            # Effacer la ligne du haut
            for x in range(BOARD_WIDTH):
                self.grid[0][x] = None
        
        return len(lines_to_clear)
    
    def update_fall_speed(self):
        # La vitesse de base diminue avec le niveau (tombe plus vite)
        base_speed = max(0.1, 1.0 - (self.level-1) * 0.05)
        self.fall_speed = base_speed * self.speed_modifier
    
    def apply_slowdown(self):
        """Ralentit la vitesse de chute de 20% pendant 10 secondes"""
        self.speed_modifier = 1.2  # 20% plus lent
        self.update_fall_speed()
        
        # Annuler le timer précédent s'il existe
        if self.speed_modifier_timer:
            self.speed_modifier_timer.cancel()
        
        # Créer un nouveau timer pour revenir à la vitesse normale
        self.speed_modifier_timer = threading.Timer(10.0, self.reset_speed)
        self.speed_modifier_timer.daemon = True
        self.speed_modifier_timer.start()
    
    def reset_speed(self):
        """Réinitialise la vitesse de chute à la normale"""
        self.speed_modifier = 1.0
        self.update_fall_speed()
        self.speed_modifier_timer = None
    
    def toggle_rainbow_mode(self, enable):
        """Active ou désactive le mode arc-en-ciel"""
        self.rainbow_mode = enable

# Classe pour le joueur humain
class HumanPlayer:
    def __init__(self, board):
        self.board = board
        self.name = "Humain"
    
    # Pas besoin d'implémenter de logique ici car le joueur contrôle via les touches

# Classe pour le joueur IA
class AIPlayer:
    def __init__(self, board):
        self.board = board
        self.name = "IA"
        self.thinking = False
    
    def make_move(self):
        """Logique simple pour l'IA pour jouer au Tetris"""
        if self.thinking or not self.board.current_piece or self.board.game_over:
            return
        
        self.thinking = True
        
        # Simuler un temps de "réflexion" pour l'IA
        threading.Timer(AI_THINKING_TIME, self._execute_move).start()
    
    def _execute_move(self):
        """Exécute le meilleur mouvement déterminé par l'IA"""
        if self.board.game_over:
            self.thinking = False
            return
            
        best_score = -float('inf')
        best_rotation = 0
        best_x = 0
        
        # Tester toutes les rotations et positions possibles
        original_piece = copy.deepcopy(self.board.current_piece)
        
        for rotation in range(len(SHAPES[original_piece.shape_name])):
            # Faire tourner la pièce jusqu'à la rotation actuelle
            test_piece = copy.deepcopy(original_piece)
            for _ in range(rotation):
                test_piece.rotate()
                
            # Tester chaque position horizontale possible
            min_x = -test_piece.x
            max_x = BOARD_WIDTH - max(x for x, _ in test_piece.get_blocks()) - 1
            
            for test_x in range(min_x, max_x + 1):
                # Créer une copie de la pièce pour les tests
                test_piece = copy.deepcopy(original_piece)
                for _ in range(rotation):
                    test_piece.rotate()
                
                # Déplacer la pièce horizontalement
                test_piece.x += test_x
                
                # Faire tomber la pièce jusqu'en bas
                landing_y = 0
                while True:
                    test_piece.y += 1
                    if not self._is_valid_position(test_piece):
                        test_piece.y -= 1
                        landing_y = test_piece.y
                        break
                
                # Évaluer cette position
                score = self._evaluate_position(test_piece)
                
                if score > best_score:
                    best_score = score
                    best_rotation = rotation
                    best_x = test_x
        
        # Exécuter le meilleur mouvement
        for _ in range(best_rotation):
            self.board.try_rotate()
        
        # Déplacer horizontalement
        dx = best_x
        if dx < 0:
            for _ in range(abs(dx)):
                self.board.try_move(-1, 0)
        else:
            for _ in range(dx):
                self.board.try_move(1, 0)
        
        # Faire tomber la pièce jusqu'en bas
        while self.board.try_move(0, 1):
            pass
        
        self.thinking = False
    
    def _is_valid_position(self, piece):
        """Vérifie si la position d'une pièce est valide"""
        blocks = piece.get_blocks()
        
        for x, y in blocks:
            # Vérifier si la position est valide
            if (x < 0 or x >= BOARD_WIDTH or 
                y < 0 or y >= BOARD_HEIGHT or
                (y >= 0 and self.board.grid[y][x] is not None)):
                return False
                
        return True
    
    def _evaluate_position(self, piece):
        """Évalue la qualité d'une position pour la pièce"""
        # Simuler l'ajout de la pièce à la grille
        test_grid = [row[:] for row in self.board.grid]
        score = 0
        
        for x, y in piece.get_blocks():
            if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                test_grid[y][x] = piece.color
        
        # Critères d'évaluation
        
        # 1. Nombre de lignes complétées
        lines_cleared = 0
        for y in range(BOARD_HEIGHT):
            if all(test_grid[y][x] is not None for x in range(BOARD_WIDTH)):
                lines_cleared += 1
                score += 100  # Bonus pour chaque ligne complétée
        
        # 2. Hauteur de la pile
        pile_height = 0
        for y in range(BOARD_HEIGHT):
            if any(test_grid[y][x] is not None for x in range(BOARD_WIDTH)):
                pile_height = BOARD_HEIGHT - y
                break
        
        score -= pile_height * 2  # Pénalité pour la hauteur
        
        # 3. Nombre de trous (cellules vides avec des blocs au-dessus)
        holes = 0
        for x in range(BOARD_WIDTH):
            found_block = False
            for y in range(BOARD_HEIGHT):
                if test_grid[y][x] is not None:
                    found_block = True
                elif found_block:
                    holes += 1
        
        score -= holes * 5  # Pénalité importante pour les trous
        
        # 4. Nombre de blocs adjacents (pour favoriser le regroupement)
        adjacencies = 0
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                if test_grid[y][x] is not None:
                    # Vérifier les 4 directions
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx, y + dy
                        if (0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT and 
                            test_grid[ny][nx] is not None):
                            adjacencies += 1
        
        score += adjacencies  # Bonus pour les blocs adjacents
        
        # 5. Bonus pour les pièces spéciales bien placées
        if piece.is_special():
            score += 50  # Bonus supplémentaire pour placer une pièce spéciale
        
        return score

# Classe principale du jeu Tetris
class TetrisGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Tetris à deux joueurs")
        # Augmenter la marge verticale de 100 à 150 ou 200 pixels
        self.root.geometry(f"{2*BOARD_WIDTH*BLOCK_SIZE + 300}x{BOARD_HEIGHT*BLOCK_SIZE + 200}")
        self.root.configure(bg='black')
        self.root.resizable(False, False)
        
        # Créer les plateaux
        self.human_board = Board()
        self.ai_board = Board()
        
        # Créer les joueurs
        self.human_player = HumanPlayer(self.human_board)
        self.ai_player = AIPlayer(self.ai_board)
        
        # Configuration de l'interface
        self.setup_ui()
        
        # Variables pour le jeu
        self.game_running = False
        self.fall_timer = None
        self.ai_timer = None
        self.rainbow_timer = None
        self.rainbow_end_timer = None
        self.rainbow_counter = 0
        
        # Lier les touches pour le contrôle du joueur
        self.root.bind("<Left>", lambda e: self.move_human_piece(-1, 0))
        self.root.bind("<Right>", lambda e: self.move_human_piece(1, 0))
        self.root.bind("<Down>", lambda e: self.move_human_piece(0, 1))
        self.root.bind("<Up>", lambda e: self.rotate_human_piece())
        self.root.bind("<space>", lambda e: self.drop_human_piece())
        self.root.bind("<p>", lambda e: self.toggle_pause())
        self.root.bind("<r>", lambda e: self.restart_game())
        
        # Démarrer le jeu
        self.start_game()
    
    def setup_ui(self):
        # Cadre principal
        main_frame = tk.Frame(self.root, bg='black')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cadre pour le joueur humain
        human_frame = tk.Frame(main_frame, bg='#111111', bd=2, relief=tk.RAISED)
        human_frame.pack(side=tk.LEFT, padx=5)
        
        human_label = tk.Label(human_frame, text="JOUEUR", font=("Arial", 16, "bold"), bg='#111111', fg='white')
        human_label.pack(pady=5)
        
        self.human_score_label = tk.Label(human_frame, text="Score: 0", font=("Arial", 12), bg='#111111', fg='white')
        self.human_score_label.pack()
        
        self.human_level_label = tk.Label(human_frame, text="Niveau: 1", font=("Arial", 12), bg='#111111', fg='white')
        self.human_level_label.pack(pady=5)
        
        self.human_canvas = tk.Canvas(
            human_frame, 
            width=BOARD_WIDTH*BLOCK_SIZE, 
            height=BOARD_HEIGHT*BLOCK_SIZE,
            bg='black',
            highlightthickness=1,
            highlightbackground='#555555'
        )
        self.human_canvas.pack()
        
        # Section d'informations et contrôles au milieu
        info_frame = tk.Frame(main_frame, bg='black', width=200)
        info_frame.pack(side=tk.LEFT, fill=tk.BOTH, padx=10)
        
        # Informations de contrôle
        controls_label = tk.Label(info_frame, text="CONTRÔLES", font=("Arial", 14, "bold"), bg='black', fg='white')
        controls_label.pack(pady=10)
        
        controls_text = """
        ← → : Déplacer
        ↑ : Rotation
        ↓ : Descendre
        Espace : Tomber
        P : Pause
        R : Recommencer
        """
        
        controls_info = tk.Label(info_frame, text=controls_text, font=("Arial", 10), bg='black', fg='white', justify=tk.LEFT)
        controls_info.pack(pady=5)
        
        # Section "Prochain"
        next_label = tk.Label(info_frame, text="PROCHAIN", font=("Arial", 14, "bold"), bg='black', fg='white')
        next_label.pack(pady=10)
        
        self.next_piece_canvas = tk.Canvas(
            info_frame, 
            width=4*BLOCK_SIZE, 
            height=4*BLOCK_SIZE,
            bg='black',
            highlightthickness=1,
            highlightbackground='#555555'
        )
        self.next_piece_canvas.pack()
        
        # Boutons
        self.pause_button = tk.Button(info_frame, text="Pause (P)", command=self.toggle_pause, bg='#333333', fg='white')
        self.pause_button.pack(pady=10, fill=tk.X)
        
        self.restart_button = tk.Button(info_frame, text="Recommencer (R)", command=self.restart_game, bg='#333333', fg='white')
        self.restart_button.pack(fill=tk.X)
        
        # Affichage du statut
        self.status_label = tk.Label(info_frame, text="Prêt", font=("Arial", 12), bg='black', fg='white')
        self.status_label.pack(pady=20)
        
        # Cadre pour l'IA
        ai_frame = tk.Frame(main_frame, bg='#111111', bd=2, relief=tk.RAISED)
        ai_frame.pack(side=tk.RIGHT, padx=5)
        
        ai_label = tk.Label(ai_frame, text="IA", font=("Arial", 16, "bold"), bg='#111111', fg='white')
        ai_label.pack(pady=5)
        
        self.ai_score_label = tk.Label(ai_frame, text="Score: 0", font=("Arial", 12), bg='#111111', fg='white')
        self.ai_score_label.pack()
        
        self.ai_level_label = tk.Label(ai_frame, text="Niveau: 1", font=("Arial", 12), bg='#111111', fg='white')
        self.ai_level_label.pack(pady=5)
        
        self.ai_canvas = tk.Canvas(
            ai_frame, 
            width=BOARD_WIDTH*BLOCK_SIZE, 
            height=BOARD_HEIGHT*BLOCK_SIZE,
            bg='black',
            highlightthickness=1,
            highlightbackground='#555555'
        )
        self.ai_canvas.pack()
    
    def start_game(self):
        """Démarre une nouvelle partie"""
        # Initialisation des plateaux
        self.human_board = Board()
        self.ai_board = Board()
        
        # Mise à jour des joueurs
        self.human_player.board = self.human_board
        self.ai_player.board = self.ai_board
        
        # Création des premières pièces
        self.human_board.new_piece()
        self.ai_board.new_piece()
        
        # Mise à jour des affichages
        self.update_human_board()
        self.update_ai_board()
        self.update_next_piece()
        self.update_score_display()
        
        # Démarrage des timers
        self.game_running = True
        self.start_fall_timer()
        self.start_ai_timer()
        self.start_rainbow_timer()
        
        self.status_label.config(text="Jeu en cours")
    
    def restart_game(self):
        """Redémarre le jeu"""
        # Annuler tous les timers
        self.cancel_timers()
        
        # Démarrer une nouvelle partie
        self.start_game()
    
    def toggle_pause(self):
        """Met le jeu en pause ou le reprend"""
        if self.game_running:
            self.game_running = False
            self.cancel_timers()
            self.status_label.config(text="Pause")
            self.pause_button.config(text="Reprendre (P)")
        else:
            self.game_running = True
            self.start_fall_timer()
            self.start_ai_timer()
            self.start_rainbow_timer()
            self.status_label.config(text="Jeu en cours")
            self.pause_button.config(text="Pause (P)")
    
    def cancel_timers(self):
        """Annule tous les timers du jeu"""
        if self.fall_timer:
            self.root.after_cancel(self.fall_timer)
            self.fall_timer = None
            
        if self.ai_timer:
            self.root.after_cancel(self.ai_timer)
            self.ai_timer = None
            
        if self.rainbow_timer:
            self.root.after_cancel(self.rainbow_timer)
            self.rainbow_timer = None
            
        if self.rainbow_end_timer:
            self.root.after_cancel(self.rainbow_end_timer)
            self.rainbow_end_timer = None
    
    def start_fall_timer(self):
        """Démarre le timer pour la chute des pièces"""
        if not self.game_running:
            return
            
        self.fall_timer = self.root.after(int(self.human_board.fall_speed * 1000), self.piece_fall)
    
    def start_ai_timer(self):
        """Démarre le timer pour les mouvements de l'IA"""
        if not self.game_running:
            return
            
        self.ai_timer = self.root.after(int(self.ai_board.fall_speed * 1000), self.ai_play)
    
    def start_rainbow_timer(self):
        """Démarre le timer pour l'effet arc-en-ciel"""
        if not self.game_running:
            return
            
        # L'effet arc-en-ciel se déclenche toutes les 2 minutes
        self.rainbow_timer = self.root.after(RAINBOW_INTERVAL * 1000, self.activate_rainbow)
    
    def activate_rainbow(self):
        """Active l'effet arc-en-ciel"""
        self.human_board.toggle_rainbow_mode(True)
        self.ai_board.toggle_rainbow_mode(True)
        self.status_label.config(text="Mode Arc-en-ciel!")
        
        # Mettre à jour les affichages
        self.update_human_board()
        self.update_ai_board()
        
        # Timer pour désactiver l'effet après 20 secondes
        self.rainbow_end_timer = self.root.after(RAINBOW_DURATION * 1000, self.deactivate_rainbow)
    
    def deactivate_rainbow(self):
        """Désactive l'effet arc-en-ciel"""
        self.human_board.toggle_rainbow_mode(False)
        self.ai_board.toggle_rainbow_mode(False)
        self.status_label.config(text="Jeu en cours")
        
        # Mettre à jour les affichages
        self.update_human_board()
        self.update_ai_board()
        
        # Redémarrer le timer arc-en-ciel
        self.start_rainbow_timer()
    
    def piece_fall(self):
        """Fait tomber les pièces d'un cran"""
        if not self.game_running:
            return
            
        # Pièce du joueur humain
        if not self.human_board.try_move(0, 1):
            # La pièce ne peut plus descendre, on la verrouille
            lines_cleared = self.human_board.lock_piece()
            
            # Vérifier les règles spéciales
            if lines_cleared == 2:
                # Cadeau surprise: l'adversaire reçoit une pièce facile
                self.ai_board.next_piece = Piece(random.choice(self.ai_board.easy_piece_types))
            
            # Vérifier si le score a atteint un multiple de 1000
            if self.human_board.score // 1000 > (self.human_board.score - lines_cleared * 50) // 1000:
                # Ralentir les deux joueurs
                self.human_board.apply_slowdown()
                self.ai_board.apply_slowdown()
                self.status_label.config(text="Ralentissement!")
            
            # Créer une nouvelle pièce
            if not self.human_board.new_piece():
                self.game_over("L'IA a gagné!")
                return
                
            self.update_next_piece()
            
        self.update_human_board()
        self.update_score_display()
        
        # Vérifier si le jeu est terminé
        if self.human_board.game_over:
            self.game_over("L'IA a gagné!")
            return
            
        # Relancer le timer
        self.start_fall_timer()
    
    def ai_play(self):
        """Fait jouer l'IA"""
        if not self.game_running or self.ai_board.game_over:
            return
            
        # Si l'IA n'est pas en train de réfléchir, faire un mouvement
        if not self.ai_player.thinking:
            self.ai_player.make_move()
        
        # Faire tomber la pièce de l'IA
        if not self.ai_board.try_move(0, 1):
            # La pièce ne peut plus descendre, on la verrouille
            lines_cleared = self.ai_board.lock_piece()
            
            # Vérifier les règles spéciales
            if lines_cleared == 2:
                # Cadeau surprise: l'adversaire reçoit une pièce facile
                self.human_board.next_piece = Piece(random.choice(self.human_board.easy_piece_types))
            
            # Vérifier si le score a atteint un multiple de 1000
            if self.ai_board.score // 1000 > (self.ai_board.score - lines_cleared * 50) // 1000:
                # Ralentir les deux joueurs
                self.human_board.apply_slowdown()
                self.ai_board.apply_slowdown()
                self.status_label.config(text="Ralentissement!")
            
            # Créer une nouvelle pièce
            if not self.ai_board.new_piece():
                self.game_over("Vous avez gagné!")
                return
        
        self.update_ai_board()
        self.update_score_display()
        
        # Vérifier si le jeu est terminé
        if self.ai_board.game_over:
            self.game_over("Vous avez gagné!")
            return
            
        # Relancer le timer
        self.start_ai_timer()
    
    def update_human_board(self):
        """Met à jour l'affichage du plateau du joueur humain"""
        self.human_canvas.delete("all")
        
        # Dessiner la grille
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.human_board.grid[y][x] if self.human_board.grid[y][x] else COLORS['EMPTY']
                
                # Effet arc-en-ciel
                if self.human_board.rainbow_mode and self.human_board.grid[y][x]:
                    hue = (self.rainbow_counter + x + y) % 360
                    color = self._hsv_to_rgb(hue, 1.0, 1.0)
                    
                self.draw_block(self.human_canvas, x, y, color)
        
        # Dessiner la pièce courante
        if self.human_board.current_piece:
            for x, y in self.human_board.current_piece.get_blocks():
                if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                    color = self.human_board.current_piece.color
                    
                    # Effet arc-en-ciel
                    if self.human_board.rainbow_mode:
                        hue = (self.rainbow_counter + x + y) % 360
                        color = self._hsv_to_rgb(hue, 1.0, 1.0)
                        
                    self.draw_block(self.human_canvas, x, y, color)
    
    def update_ai_board(self):
        """Met à jour l'affichage du plateau de l'IA"""
        self.ai_canvas.delete("all")
        
        # Dessiner la grille
        for y in range(BOARD_HEIGHT):
            for x in range(BOARD_WIDTH):
                color = self.ai_board.grid[y][x] if self.ai_board.grid[y][x] else COLORS['EMPTY']
                
                # Effet arc-en-ciel
                if self.ai_board.rainbow_mode and self.ai_board.grid[y][x]:
                    hue = (self.rainbow_counter + x + y) % 360
                    color = self._hsv_to_rgb(hue, 1.0, 1.0)
                    
                self.draw_block(self.ai_canvas, x, y, color)
        
        # Dessiner la pièce courante
        if self.ai_board.current_piece:
            for x, y in self.ai_board.current_piece.get_blocks():
                if 0 <= y < BOARD_HEIGHT and 0 <= x < BOARD_WIDTH:
                    color = self.ai_board.current_piece.color
                    
                    # Effet arc-en-ciel
                    if self.ai_board.rainbow_mode:
                        hue = (self.rainbow_counter + x + y) % 360
                        color = self._hsv_to_rgb(hue, 1.0, 1.0)
                        
                    self.draw_block(self.ai_canvas, x, y, color)
    
    def update_next_piece(self):
        """Met à jour l'affichage de la prochaine pièce"""
        self.next_piece_canvas.delete("all")
        
        if self.human_board.next_piece:
            # Obtenir les coordonnées de la forme
            shape = SHAPES[self.human_board.next_piece.shape_name][0]
            
            # Trouver les dimensions de la pièce
            min_x = min(x for x, _ in shape)
            max_x = max(x for x, _ in shape)
            min_y = min(y for _, y in shape)
            max_y = max(y for _, y in shape)
            
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            
            # Calculer le décalage pour centrer la pièce
            offset_x = (4 - width) // 2
            offset_y = (4 - height) // 2
            
            # Dessiner la pièce
            for x, y in shape:
                self.next_piece_canvas.create_rectangle(
                    (x - min_x + offset_x) * BLOCK_SIZE,
                    (y - min_y + offset_y) * BLOCK_SIZE,
                    (x - min_x + offset_x + 1) * BLOCK_SIZE,
                    (y - min_y + offset_y + 1) * BLOCK_SIZE,
                    fill=self.human_board.next_piece.color,
                    outline='white',
                    width=1
                )
    
    def update_score_display(self):
        """Met à jour l'affichage des scores"""
        self.human_score_label.config(text=f"Score: {self.human_board.score}")
        self.human_level_label.config(text=f"Niveau: {self.human_board.level}")
        
        self.ai_score_label.config(text=f"Score: {self.ai_board.score}")
        self.ai_level_label.config(text=f"Niveau: {self.ai_board.level}")
        
        # Mettre à jour le compteur arc-en-ciel
        if self.human_board.rainbow_mode or self.ai_board.rainbow_mode:
            self.rainbow_counter = (self.rainbow_counter + 5) % 360
    
    def draw_block(self, canvas, x, y, color):
        """Dessine un bloc à la position spécifiée"""
        canvas.create_rectangle(
            x * BLOCK_SIZE,
            y * BLOCK_SIZE,
            (x + 1) * BLOCK_SIZE,
            (y + 1) * BLOCK_SIZE,
            fill=color,
            outline='white',
            width=1
        )
    
    def move_human_piece(self, dx, dy):
        """Déplace la pièce du joueur humain"""
        if not self.game_running or self.human_board.game_over:
            return
            
        if self.human_board.try_move(dx, dy):
            self.update_human_board()
    
    def rotate_human_piece(self):
        """Fait tourner la pièce du joueur humain"""
        if not self.game_running or self.human_board.game_over:
            return
            
        if self.human_board.try_rotate():
            self.update_human_board()
    
    def drop_human_piece(self):
        """Fait tomber la pièce du joueur humain jusqu'en bas"""
        if not self.game_running or self.human_board.game_over:
            return
            
        # Déplacer la pièce vers le bas jusqu'à ce qu'elle ne puisse plus descendre
        while self.human_board.try_move(0, 1):
            pass
            
        # Verrouiller la pièce
        lines_cleared = self.human_board.lock_piece()
        
        # Vérifier les règles spéciales
        if lines_cleared == 2:
            # Cadeau surprise: l'adversaire reçoit une pièce facile
            self.ai_board.next_piece = Piece(random.choice(self.ai_board.easy_piece_types))
        
        # Vérifier si le score a atteint un multiple de 1000
        if self.human_board.score // 1000 > (self.human_board.score - lines_cleared * 50) // 1000:
            # Ralentir les deux joueurs
            self.human_board.apply_slowdown()
            self.ai_board.apply_slowdown()
            self.status_label.config(text="Ralentissement!")
        
        # Créer une nouvelle pièce
        if not self.human_board.new_piece():
            self.game_over("L'IA a gagné!")
            return
            
        self.update_human_board()
        self.update_next_piece()
        self.update_score_display()
    
    def game_over(self, message):
        """Affiche un message de fin de jeu et arrête la partie"""
        self.game_running = False
        self.cancel_timers()
        
        self.status_label.config(text="Game Over")
        
        # Afficher le message de fin de jeu
        messagebox.showinfo("Game Over", f"{message}\n\nJoueur: {self.human_board.score} points\nIA: {self.ai_board.score} points")
    
    def _hsv_to_rgb(self, h, s, v):
        """Convertit une couleur HSV en couleur RGB hexadécimale"""
        h = h / 360.0
        
        if s == 0.0:
            r = g = b = v
        else:
            i = int(h * 6.0)
            f = (h * 6.0) - i
            p = v * (1.0 - s)
            q = v * (1.0 - s * f)
            t = v * (1.0 - s * (1.0 - f))
            i = i % 6
            
            if i == 0: r, g, b = v, t, p
            elif i == 1: r, g, b = q, v, p
            elif i == 2: r, g, b = p, v, t
            elif i == 3: r, g, b = p, q, v
            elif i == 4: r, g, b = t, p, v
            else: r, g, b = v, p, q
        
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return f'#{r:02x}{g:02x}{b:02x}'

# Point d'entrée principal
if __name__ == "__main__":
    root = tk.Tk()
    game = TetrisGame(root)
    root.mainloop()
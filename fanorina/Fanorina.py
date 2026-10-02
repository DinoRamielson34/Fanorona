import random
from tkinter import Button, Frame, Label, StringVar, OptionMenu

class Fanorina:
    def __init__(self, canvas):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.joueur1_pions = 0
        self.joueur2_pions = 0
        self.joueur1_mode = "placement"
        self.joueur2_mode = "placement"
        self.tour = 'joueur1'
        self.canvas = canvas
        self.points = [(100 + j*150, 100 + i*150) for i in range(3) for j in range(3)]
        self.draw_board()
        self.selected_piece = None
        self.game_over = False
        
        # Mode de jeu (par défaut humain vs IA)
        self.game_mode = "human_vs_ia"
        
        # Création des boutons et de l'interface
        self.create_interface()
        
        # Variable pour suivre si le point noir a été utilisé
        self.point_noir_used = False
        self.placing_point_noir = False
        
        # Pour le mode IA vs IA
        self.ia_thinking = False

    def create_interface(self):
        # Bouton pour recommencer
        self.restart_button = Button(self.canvas.master, text="Recommencer", command=self.recommencer)
        self.restart_button.place(x=50, y=500)
        
        # Bouton pour le point noir
        self.point_noir_button = Button(self.canvas.master, text="Placer point noir", command=self.activate_point_noir)
        self.point_noir_button.place(x=320, y=500)
        
        # Menu déroulant pour choisir le mode de jeu
        self.mode_var = StringVar(self.canvas.master)
        self.mode_var.set("Humain vs IA")  # mode par défaut
        
        self.mode_menu = OptionMenu(self.canvas.master, self.mode_var, 
                                   "Humain vs IA", "Humain vs Humain", "IA vs IA", 
                                   command=self.change_game_mode)
        self.mode_menu.place(x=150, y=500)
        
        # Bouton pour lancer le mode IA vs IA
        self.ia_vs_ia_button = Button(self.canvas.master, text="Tour suivant IA", command=self.next_ia_move)
        self.ia_vs_ia_button.place(x=450, y=500)
        self.ia_vs_ia_button.config(state="disabled")

    def change_game_mode(self, selection):
        """Change le mode de jeu selon la sélection"""
        if selection == "Humain vs IA":
            self.game_mode = "human_vs_ia"
            self.ia_vs_ia_button.config(state="disabled")
        elif selection == "Humain vs Humain":
            self.game_mode = "human_vs_human"
            self.ia_vs_ia_button.config(state="disabled")
        elif selection == "IA vs IA":
            self.game_mode = "ia_vs_ia"
            self.ia_vs_ia_button.config(state="normal")
            
        # Recommencer le jeu avec le nouveau mode
        self.recommencer()

    def draw_board(self):
        for i in range(3):
            self.canvas.create_line(100, 100 + i*150, 400, 100 + i*150, width=2)
        for j in range(3):
            self.canvas.create_line(100 + j*150, 100, 100 + j*150, 400, width=2)
        for (x, y) in self.points:
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="black")

    def clic(self, event):
        if self.game_over or self.ia_thinking:
            return
            
        # Si on est en mode IA vs IA, ignorer les clics
        if self.game_mode == "ia_vs_ia":
            return
            
        # Si le mode point noir est activé
        if self.placing_point_noir:
            for idx, (x, y) in enumerate(self.points):
                if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                    i, j = divmod(idx, 3)
                    if self.board[i][j] == '':  # Vérifier que la case est vide
                        self.board[i][j] = 'N'  # N pour point Noir
                        self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill="black")
                        self.point_noir_used = True
                        self.placing_point_noir = False
                        self.point_noir_button.config(state="disabled")
                        return

        # Si c'est le tour de l'IA et on est en mode humain vs IA, ignorer les clics
        if self.tour == 'joueur2' and self.game_mode == "human_vs_ia":
            return
            
        for idx, (x, y) in enumerate(self.points):
            if abs(event.x - x) < 20 and abs(event.y - y) < 20:
                i, j = divmod(idx, 3)
                
                # Vérifier si c'est la case centrale au premier tour
                is_center = (i == 1 and j == 1)
                
                # Déterminer le joueur actuel et son mode
                joueur_actuel = 'V' if self.tour == 'joueur1' else 'R'
                mode_actuel = self.joueur1_mode if self.tour == 'joueur1' else self.joueur2_mode
                pions_count = self.joueur1_pions if self.tour == 'joueur1' else self.joueur2_pions
                
                if mode_actuel == "placement" and self.board[i][j] == '':
                    # Au début du jeu, on ne peut pas placer au centre
                    if is_center and self.joueur1_pions == 0 and self.joueur2_pions == 0:
                        self.canvas.create_text(250, 50, text="Impossible de placer au centre en début de partie", 
                                              fill="red", tags="error_msg")
                        self.canvas.after(1500, lambda: self.canvas.delete("error_msg"))
                        return
                    
                    # Vérifier si la position a un côté libre
                    if self.has_adjacent_empty_side(i, j):
                        self.board[i][j] = joueur_actuel
                        self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, 
                                              fill="green" if joueur_actuel == 'V' else "red")
                        
                        # Incrémenter le compteur de pions pour le joueur actuel
                        if self.tour == 'joueur1':
                            self.joueur1_pions += 1
                            if self.joueur1_pions >= 3:
                                self.joueur1_mode = "deplacement"
                        else:
                            self.joueur2_pions += 1
                            if self.joueur2_pions >= 3:
                                self.joueur2_mode = "deplacement"
                                
                        # Vérifier victoire
                        if self.check_victory(joueur_actuel):
                            self.end_game(f"Le joueur {1 if self.tour == 'joueur1' else 2} a gagné !")
                            return
                            
                        # Passer au joueur suivant
                        self.switch_player()
                        
                    else:
                        # Informer que le placement n'est pas valide (côté non libre)
                        self.canvas.create_text(250, 50, text="Placement invalide: besoin d'un côté libre", 
                                              fill="red", tags="error_msg")
                        self.canvas.after(1500, lambda: self.canvas.delete("error_msg"))
                elif mode_actuel == "deplacement":
                    if self.selected_piece:
                        old_i, old_j = self.selected_piece
                        if self.board[i][j] == '':
                            # Vérifier si le déplacement est valide (adjacent et côté libre)
                            if self.is_valid_move(old_i, old_j, i, j):
                                self.board[i][j] = joueur_actuel
                                self.board[old_i][old_j] = ''
                                self.redessiner_plateau()
                                self.selected_piece = None
                                
                                # Vérifier victoire
                                if self.check_victory(joueur_actuel):
                                    self.end_game(f"Le joueur {1 if self.tour == 'joueur1' else 2} a gagné !")
                                    return
                                    
                                # Passer au joueur suivant
                                self.switch_player()
                            else:
                                # Informer que le déplacement n'est pas valide
                                self.canvas.create_text(250, 50, text="Déplacement invalide", 
                                                      fill="red", tags="error_msg")
                                self.canvas.after(1500, lambda: self.canvas.delete("error_msg"))
                                self.selected_piece = None
                        else:
                            self.selected_piece = None
                    elif self.board[i][j] == joueur_actuel:
                        self.selected_piece = (i, j)
                break

    def switch_player(self):
        """Passe au joueur suivant et lance l'IA si nécessaire"""
        self.tour = 'joueur2' if self.tour == 'joueur1' else 'joueur1'
        
        # Si c'est le tour de l'IA en mode humain vs IA
        if self.tour == 'joueur2' and self.game_mode == "human_vs_ia":
            self.ia_thinking = True
            self.canvas.after(500, self.ia_joue)

    def has_adjacent_empty_side(self, i, j):
        """Vérifie si une position a au moins un côté adjacent vide (hors plateau = côté libre)"""
        # Pour la case centrale (1,1), vérifier spécifiquement les 4 cases adjacentes
        if i == 1 and j == 1:
            return (self.board[0][1] == '' or  # haut
                    self.board[1][0] == '' or  # gauche
                    self.board[1][2] == '' or  # droite
                    self.board[2][1] == '')    # bas
                    
        # Pour les autres cases:
        # Vérifier les quatre côtés (haut, bas, gauche, droite)
        # Si la position est sur le bord du plateau, ce côté est considéré comme libre
        
        # Côté gauche
        if j == 0 or self.board[i][j-1] == '':
            return True
        # Côté droit
        if j == 2 or self.board[i][j+1] == '':
            return True
        # Côté haut
        if i == 0 or self.board[i-1][j] == '':
            return True
        # Côté bas
        if i == 2 or self.board[i+1][j] == '':
            return True
        
        return False

    def is_valid_move(self, old_i, old_j, new_i, new_j):
        """Vérifie si un déplacement est valide: cases adjacentes orthogonalement et destination avec côté libre"""
        # Vérifier que la destination est vide
        if self.board[new_i][new_j] != '':
            return False
            
        # Vérifier que le déplacement est orthogonal et adjacent
        if abs(old_i - new_i) + abs(old_j - new_j) != 1:
            return False
            
        # Vérifier que la destination a un côté libre
        return self.has_adjacent_empty_side(new_i, new_j)

    def redessiner_plateau(self):
        self.canvas.delete("all")
        self.draw_board()
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == 'V':
                    x, y = self.points[i * 3 + j]
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="green")
                elif self.board[i][j] == 'R':
                    x, y = self.points[i * 3 + j]
                    self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="red")
                elif self.board[i][j] == 'N':  # Dessiner le point noir
                    x, y = self.points[i * 3 + j]
                    self.canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill="black")

    def next_ia_move(self):
        """Lance le prochain tour de l'IA en mode IA vs IA"""
        if self.game_mode == "ia_vs_ia" and not self.game_over and not self.ia_thinking:
            self.ia_thinking = True
            self.canvas.after(500, self.ia_joue)

    def ia_joue(self):
        """Fait jouer l'IA"""
        if self.game_over:
            self.ia_thinking = False
            return
            
        # Détermine quel joueur est l'IA
        joueur_ia = 'R'  # En mode humain vs IA, l'IA joue toujours rouge
        if self.game_mode == "ia_vs_ia":
            joueur_ia = 'V' if self.tour == 'joueur1' else 'R'
            
        # Détermine le mode de l'IA (placement ou déplacement)
        mode_ia = self.joueur1_mode if self.tour == 'joueur1' else self.joueur2_mode
        pions_count = self.joueur1_pions if self.tour == 'joueur1' else self.joueur2_pions
        
        if mode_ia == "placement":
            if pions_count < 3:  # Limiter à 3 pions
                # Utiliser minimax pour la phase de placement
                best_score = float('-inf')
                best_move = None
                
                for i in range(3):
                    for j in range(3):
                        # Vérifier si la case est libre et a un côté libre
                        if self.board[i][j] == '' and self.has_adjacent_empty_side(i, j):
                            # Vérifier la règle du centre - impossible en début de partie
                            if (i == 1 and j == 1 and self.joueur1_pions == 0 and 
                                self.joueur2_pions == 0):
                                continue
                                
                            self.board[i][j] = joueur_ia
                            score = self.minimax(self.board, 3, False, joueur_ia)
                            self.board[i][j] = ''
                            
                            if score > best_score:
                                best_score = score
                                best_move = (i, j)
                
                if best_move:
                    i, j = best_move
                    self.board[i][j] = joueur_ia
                    
                    # Incrémenter le compteur de pions
                    if self.tour == 'joueur1':
                        self.joueur1_pions += 1
                        if self.joueur1_pions >= 3:
                            self.joueur1_mode = "deplacement"
                    else:
                        self.joueur2_pions += 1
                        if self.joueur2_pions >= 3:
                            self.joueur2_mode = "deplacement"
                            
                    self.redessiner_plateau()
                    
                    # Vérifier victoire
                    if self.check_victory(joueur_ia):
                        self.end_game(f"Le joueur {1 if self.tour == 'joueur1' else 2} (IA) a gagné !")
                        self.ia_thinking = False
                        return
                        
                    # Passer au joueur suivant
                    self.switch_player()
                else:
                    # Aucun mouvement valide n'a été trouvé
                    self.end_game("Match nul - aucun mouvement valide pour l'IA")
                    self.ia_thinking = False
                    return
            else:
                # Changer le mode de l'IA
                if self.tour == 'joueur1':
                    self.joueur1_mode = "deplacement"
                else:
                    self.joueur2_mode = "deplacement"
                self.ia_joue()  # Réexécuter pour jouer en mode déplacement
                return
        
        elif mode_ia == "deplacement":
            # Utiliser minimax pour la phase de déplacement
            best_score = float('-inf')
            best_move = None
            
            # Trouver tous les pions de l'IA et générer tous les déplacements possibles
            for old_i in range(3):
                for old_j in range(3):
                    if self.board[old_i][old_j] == joueur_ia:
                        # Vérifier les déplacements orthogonaux
                        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            new_i, new_j = old_i + di, old_j + dj
                            # Vérifier si la destination est valide
                            if (0 <= new_i < 3 and 0 <= new_j < 3 and 
                                self.board[new_i][new_j] == ''):
                                if self.has_adjacent_empty_side(new_i, new_j):
                                    # Simuler le déplacement
                                    self.board[old_i][old_j] = ''
                                    self.board[new_i][new_j] = joueur_ia
                                    
                                    # Évaluer ce déplacement
                                    score = self.minimax(self.board, 3, False, joueur_ia)
                                    
                                    # Annuler le déplacement
                                    self.board[old_i][old_j] = joueur_ia
                                    self.board[new_i][new_j] = ''
                                    
                                    if score > best_score:
                                        best_score = score
                                        best_move = (old_i, old_j, new_i, new_j)
            
            if best_move:
                old_i, old_j, new_i, new_j = best_move
                # Déplacer le pion
                self.board[old_i][old_j] = ''
                self.board[new_i][new_j] = joueur_ia
                
                self.redessiner_plateau()
                
                # Vérifier victoire
                if self.check_victory(joueur_ia):
                    self.end_game(f"Le joueur {1 if self.tour == 'joueur1' else 2} (IA) a gagné !")
                    self.ia_thinking = False
                    return
                    
                # Passer au joueur suivant
                self.switch_player()
            else:
                # Aucun mouvement valide n'a été trouvé
                self.end_game("Match nul - aucun mouvement valide pour l'IA")
                self.ia_thinking = False
                return
        
        self.ia_thinking = False

    def has_adjacent_empty_side_on_board(self, board, i, j):
        """Vérifie si une position a au moins un côté adjacent vide sur un plateau donné"""
        # Pour la case centrale (1,1), vérifier spécifiquement les 4 cases adjacentes
        if i == 1 and j == 1:
            return (board[0][1] == '' or  # haut
                    board[1][0] == '' or  # gauche
                    board[1][2] == '' or  # droite
                    board[2][1] == '')    # bas
                    
        # Pour les autres cases
        # Côté gauche
        if j == 0 or board[i][j-1] == '':
            return True
        # Côté droit
        if j == 2 or board[i][j+1] == '':
            return True
        # Côté haut
        if i == 0 or board[i-1][j] == '':
            return True
        # Côté bas
        if i == 2 or board[i+1][j] == '':
            return True
        
        return False

    def minimax(self, board, depth, is_maximizing, ia_player, alpha=float('-inf'), beta=float('inf')):
        """
        Algorithme minimax adapté pour fonctionner avec n'importe quel joueur IA
        ia_player est 'V' ou 'R' selon qui est l'IA
        """
        human_player = 'R' if ia_player == 'V' else 'V'
        
        # Vérifier s'il y a une victoire ou si la profondeur est atteinte
        if self.check_victory_on_board(board, ia_player):
            return 100 + depth  # L'IA gagne (valeur positive élevée)
        elif self.check_victory_on_board(board, human_player):
            return -100 - depth  # L'adversaire gagne (valeur négative)
        elif depth == 0:
            return self.evaluate_board(board, ia_player)  # Évaluation de la position
        
        if is_maximizing:  # Tour de l'IA (maximise le score)
            max_eval = float('-inf')
            moves_found = False
            
            # Phase de déplacement pour l'IA
            for i in range(3):
                for j in range(3):
                    if board[i][j] == ia_player:
                        # Vérifier les déplacements orthogonaux
                        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < 3 and 0 <= nj < 3 and board[ni][nj] == '':
                                # Vérifier si la destination a un côté libre
                                temp_board = [row[:] for row in board]
                                temp_board[i][j] = ''
                                if self.has_adjacent_empty_side_on_board(temp_board, ni, nj):
                                    moves_found = True
                                    # Simuler le déplacement
                                    board[i][j] = ''
                                    board[ni][nj] = ia_player
                                    
                                    # Récursion minimax
                                    eval = self.minimax(board, depth - 1, False, ia_player, alpha, beta)
                                    
                                    # Annuler le déplacement
                                    board[i][j] = ia_player
                                    board[ni][nj] = ''
                                    
                                    max_eval = max(max_eval, eval)
                                    alpha = max(alpha, eval)
                                    if beta <= alpha:
                                        break
            
            # Si aucun mouvement n'est trouvé, c'est une impasse pour l'IA
            if not moves_found:
                return -50  # Valeur négative pour éviter les impasses
            
            return max_eval
        
        else:  # Tour de l'adversaire (minimise le score)
            min_eval = float('inf')
            moves_found = False
            
            # Phase de déplacement pour l'adversaire
            for i in range(3):
                for j in range(3):
                    if board[i][j] == human_player:
                        # Vérifier les déplacements orthogonaux
                        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            ni, nj = i + di, j + dj
                            if 0 <= ni < 3 and 0 <= nj < 3 and board[ni][nj] == '':
                                # Vérifier si la destination a un côté libre
                                temp_board = [row[:] for row in board]
                                temp_board[i][j] = ''
                                if self.has_adjacent_empty_side_on_board(temp_board, ni, nj):
                                    moves_found = True
                                    # Simuler le déplacement
                                    board[i][j] = ''
                                    board[ni][nj] = human_player
                                    
                                    # Récursion minimax
                                    eval = self.minimax(board, depth - 1, True, ia_player, alpha, beta)
                                    
                                    # Annuler le déplacement
                                    board[i][j] = human_player
                                    board[ni][nj] = ''
                                    
                                    min_eval = min(min_eval, eval)
                                    beta = min(beta, eval)
                                    if beta <= alpha:
                                        break
            
            # Si aucun mouvement n'est trouvé, c'est une impasse pour l'adversaire
            if not moves_found:
                return 50  # Valeur positive pour les impasses de l'adversaire
            
            return min_eval

    def evaluate_board(self, board, ia_player):
        """
        Évalue la position du jeu pour l'IA
        Retourne une valeur positive si l'IA est en bonne position, négative sinon
        ia_player est 'V' ou 'R' selon qui est l'IA
        """
        human_player = 'R' if ia_player == 'V' else 'V'
        score = 0
        
        # Vérifier les lignes, colonnes et diagonales pour les pions alignés
        for player, value in [(ia_player, 1), (human_player, -1)]:
            # Lignes
            for i in range(3):
                row_count = board[i].count(player)
                if row_count > 0:
                    score += row_count * value * 2
                
            # Colonnes
            for j in range(3):
                col_count = sum(1 for i in range(3) if board[i][j] == player)
                if col_count > 0:
                    score += col_count * value * 2
                
            # Diagonales
            diag1 = sum(1 for i in range(3) if board[i][i] == player)
            diag2 = sum(1 for i in range(3) if board[i][2-i] == player)
            
            if diag1 > 0:
                score += diag1 * value * 3
            if diag2 > 0:
                score += diag2 * value * 3
        
        # Bonus pour le centre (après la phase initiale)
        if board[1][1] == ia_player:
            score += 3
        elif board[1][1] == human_player:
            score -= 3
            
        # Bonus pour les positions avec plus de côtés libres
        for i in range(3):
            for j in range(3):
                if board[i][j] == ia_player:
                    # Compter les côtés libres
                    free_sides = 0
                    
                    # Pour la case centrale
                    if i == 1 and j == 1:
                        if board[0][1] == '': free_sides += 1  # haut
                        if board[1][0] == '': free_sides += 1  # gauche
                        if board[1][2] == '': free_sides += 1  # droite
                        if board[2][1] == '': free_sides += 1  # bas
                    else:
                        # Pour les autres cases
                        # Gauche
                        if j == 0 or board[i][j-1] == '':
                            free_sides += 1
                        # Droite
                        if j == 2 or board[i][j+1] == '':
                            free_sides += 1
                        # Haut
                        if i == 0 or board[i-1][j] == '':
                            free_sides += 1
                        # Bas
                        if i == 2 or board[i+1][j] == '':
                            free_sides += 1
                    
                    score += free_sides * 2  # Valoriser davantage la mobilité
                    
                elif board[i][j] == human_player:
                    # Compter les côtés libres pour l'adversaire
                    free_sides = 0
                    
                    # Pour la case centrale
                    if i == 1 and j == 1:
                        if board[0][1] == '': free_sides += 1  # haut
                        if board[1][0] == '': free_sides += 1  # gauche
                        if board[1][2] == '': free_sides += 1  # droite
                        if board[2][1] == '': free_sides += 1  # bas
                    else:
                        # Pour les autres cases
                        if j == 0 or board[i][j-1] == '':
                            free_sides += 1
                        if j == 2 or board[i][j+1] == '':
                            free_sides += 1
                        if i == 0 or board[i-1][j] == '':
                            free_sides += 1
                        if i == 2 or board[i+1][j] == '':
                            free_sides += 1
                    
                    score -= free_sides * 2  # Pénaliser la mobilité de l'adversaire
            
        # Pénalité pour le point noir si présent
        for i in range(3):
            for j in range(3):
                if board[i][j] == 'N':
                    # Si le point noir est près des pions de l'IA, c'est mauvais
                    # Si le point noir est près des pions de l'IA, c'est mauvais
                    for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Seulement les cases adjacentes orthogonalement
                        ni, nj = i + di, j + dj
                        if 0 <= ni < 3 and 0 <= nj < 3:
                            if board[ni][nj] == ia_player:
                                score -= 8  # Augmenter la pénalité car le point noir bloque un côté
                            elif board[ni][nj] == human_player:
                                score += 5  # Bonus si le point noir gêne l'adversaire
        
        return score

    def check_victory(self, player):
        return self.check_victory_on_board(self.board, player)
        
    def check_victory_on_board(self, board, player):
        # Lignes
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] == player:
                return True
        # Colonnes
        for j in range(3):
            if board[0][j] == board[1][j] == board[2][j] == player:
                return True
        # Diagonales
        if board[0][0] == board[1][1] == board[2][2] == player:
            return True
        if board[0][2] == board[1][1] == board[2][0] == player:
            return True
        return False

    def end_game(self, message):
        self.canvas.create_text(250, 200, text=message, font=('Helvetica', 24), fill="black")
        self.canvas.update()
        self.game_over = True

    def recommencer(self):
        self.board = [['' for _ in range(3)] for _ in range(3)]
        self.joueur1_pions = 0
        self.joueur2_pions = 0
        self.joueur1_mode = "placement"
        self.joueur2_mode = "placement"
        self.tour = 'joueur1'
        self.game_over = False
        self.point_noir_used = False
        self.point_noir_button.config(state="normal")
        self.selected_piece = None
        self.ia_thinking = False
        self.placing_point_noir = False
        self.redessiner_plateau()
        
        # Si on est en mode IA vs IA, désactiver le bouton de point noir
        if self.game_mode == "ia_vs_ia":
            self.point_noir_button.config(state="disabled")

    def activate_point_noir(self):
        if not self.point_noir_used and not self.game_over:
            self.placing_point_noir = True
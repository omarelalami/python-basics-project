import pygame
import sys
import numpy as np

def compute_number_neighbors(pade_frame, i, j):
    number = pade_frame[i][j-1] + \
             pade_frame[i][j+1] + \
             pade_frame[i+1][j] + \
             pade_frame[i-1][j] + \
             pade_frame[i-1][j+1] + \
             pade_frame[i+1][j+1] + \
             pade_frame[i-1][j-1] + \
             pade_frame[i+1][j-1]

    return number

def compute_next_frame(frame):
    pade_frame = np.pad(frame, 1, mode='constant', constant_values=0)

    for i in range(1, len(pade_frame)-1):
        for j in range(1, len(pade_frame[0])-1):
            if pade_frame[i][j] == 0 and compute_number_neighbors(pade_frame, i, j) == 3:
                frame[i-1][j-1] = 1
            elif pade_frame[i][j] == 1 and (compute_number_neighbors(pade_frame, i, j) == 2 or compute_number_neighbors(pade_frame, i, j) == 3):
                frame[i-1][j-1] = 1
            else:
                frame[i-1][j-1] = 0

    return frame

# Initialisation de Pygame
pygame.init()

# Paramètres de la fenêtre
largeur, hauteur = 800, 800
fenetre = pygame.display.set_mode((largeur, hauteur))
pygame.display.set_caption("Menu principal")

# Couleurs
BLANC = pygame.Color("white")
NOIR = pygame.Color("black")
VERT = pygame.Color("green")

# Taille de la grille
nb_lignes, nb_colonnes = 40, 40  # Réduire la taille pour s'adapter à la nouvelle résolution
taille_case = min(largeur // nb_colonnes, hauteur // nb_lignes)

# Initialisation de la grille
grille = np.zeros((nb_lignes, nb_colonnes), dtype=int)

# Fonction pour initialiser la grille avec des cellules aléatoires
def initialiser_grille():
    return np.random.choice([0, 1], size=(nb_lignes, nb_colonnes))

grille = initialiser_grille()

# Bouton pour commencer le jeu
bouton_rect = pygame.Rect(largeur // 2 - 130, hauteur // 2 - 20, 150, 30)
cadre_rect = pygame.Rect(largeur // 2 - 80, hauteur // 2 - 30, 200, 80)  # Cadre autour du bouton
bouton_font = pygame.font.Font(None, 36)
bouton_texte = bouton_font.render("Lancer le jeu", True, NOIR)

# Texte de crédit
credit_font = pygame.font.Font(None, 50)
credit_texte = credit_font.render("Réalisé par Omar El Alami", True, NOIR)
credit_rect = credit_texte.get_rect(center=(largeur // 2, hauteur - 20))

image_path = "C:/Users/OMAR/Desktop/Hetic cours/Hackathoon/HETIC LOGO.png"  # Remplacez cela par le chemin de votre image
image = pygame.image.load(image_path)
image_rect = image.get_rect(center=(80, 50))  # Position de l'image en haut

def afficher_ecran_accueil():
    # Afficher la page d'accueil
    fenetre.fill(BLANC)
    pygame.draw.rect(fenetre, NOIR, cadre_rect, 2)  # Dessiner le cadre autour du bouton
    fenetre.blit(bouton_texte, bouton_rect.center)
    fenetre.blit(credit_texte, credit_rect)
    # Afficher l'image en haut
    fenetre.blit(image, image_rect)
    pygame.display.flip()

    attente_clic = True
    while attente_clic:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if bouton_rect.collidepoint(x, y):
                    attente_clic = False

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    afficher_ecran_accueil()

    # L'écran d'accueil a été fermé par un clic, le jeu peut commencer
    jeu_en_cours = True

    # Nouvelle boucle principale pour gérer le jeu
    while jeu_en_cours:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Calcul de la prochaine génération
        grille = compute_next_frame(grille.copy())

        # Dessiner le fond
        fenetre.fill(BLANC)

        # Dessiner la grille
        for i in range(nb_lignes):
            for j in range(nb_colonnes):
                couleur = NOIR if grille[i][j] == 1 else BLANC
                pygame.draw.rect(fenetre, couleur, (j * taille_case, i * taille_case, taille_case, taille_case))

        # Actualisation de l'écran
        pygame.display.flip()

        # Ajouter un court délai pour ralentir le déroulement du jeu
        pygame.time.delay(100)

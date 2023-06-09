# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import re

class LifeSimulator:
	"""Classe gerant la creation et l'evolution de notre espace de vie."""

	##################################################
	def __init__(self):
		"""Constructeur de la classe."""
		self.random_seed()

	##################################################
	def load(self, file):
		"""Charge un fichier ou une graine aleatoire si aucun fichier."""
		if file:
			# Chargement du fichier
			with open(file, "r") as f:
				data = f.read()
				# avec regex c'est rigolo, pour python \s ce sont les espaces, \d les nombres 
				# group(1) récupère ce qui est dnas la première parenthèse
				x = int(re.search(r"x\s*=\s*(\d+)", data).group(1))
				y = int(re.search(r"y\s*=\s*(\d+)", data).group(1))

				# Trouver toutes les coordonnées de la graine puis séparer ces coordonnées
				seed_str = re.search(r"seed\s*=\s*([^\n]+(?:\n[^\n]+)*)", data).group(1)
				seed = set((int(x), int(y)) for (x, y) in re.findall(r"\((\d+),\s*(\d+)\)", seed_str))

				# Initialisation de la grille (les coordonnées partent du bas à gauche)
				self.white_seed(x, y)
				for s in seed:	self.space[s[0], s[1]] = True
		else:
			self.random_seed()

	##################################################
	def update(self):
		"""Met a jour le tableau: 
		Si une case possede exactement 3 voisins en vie, elle s'anime.
		Si une case possede exactement 2 voisins en vie et est elle meme en vie, elle reste en vie.
		Dans les autres cas, elle meurt.
		"""
		
		# Vérification pour chaque case du tableau d'origine si les conditions sont remplis. 
		# Version utilisant les fonctions numpy de manipulation de tableau 
		spaceI = self.space.astype(int)	# Transformation en int pour compter les voisins
		count = np.zeros(spaceI.shape)	# Création d'un tableau prenant en compte les voisins
		count[1:-1,1:-1] = (spaceI[:-2,:-2]  + spaceI[:-2,1:-1] + spaceI[:-2,2:] + 
							spaceI[1:-1,:-2] +                	  spaceI[1:-1,2:] + 
							spaceI[2:,:-2]   + spaceI[2:,1:-1]  + spaceI[2:,2:]) 
		
		# count[1:-1,1:-1] permet de sélectionner le tableau excepté les bords.
		# l'opération suivante permet de calculer la somme des éléments autour de chaque case (éléments dont la valeur vaut 0 ou 1)
		# En jouant avec les indice cela permet d'effectuer une seule operation "visuellement".
		# Mais, il est possible d'utiliser une fonction de convolution (convolve) ou de parcourir le tableau dans une double boucle

		# Mise à jour de l'espace de vie, si une des deux conditions est remplit, l'élément est en vie.
		self.space = np.logical_or(count == 3,np.logical_and(spaceI == 1,count == 2))

	##################################################
	def draw(self):
		"""Dessine le tableau avec matplotlib."""
		# Affichage de la grille avec Matplotlib
		fig = plt.figure(figsize=(16,9),dpi=120)    
		# tableau[:,::-1].T			Transpose pour avoir les x sur l'axe des abscisses sur notre dessin et on inverse l'axe des ordonnées
		plt.imshow(self.space[:,::-1].T, cmap="gray_r")									# Affiche notre tableau comme une image
		plt.grid(color='lightblue', linestyle='-', linewidth=0.5)						# Affichage de la grille
		plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)	# Supprime les légendes sur X et Y
		# La légende (et donc les lignes de la grille) vont de -0.5 à MAX + 0.5 en allant de 1 en 1
		# On a 0.5 de décallage car chaque cas de notre tableau est centré sur un nombre entier et sa visualisation va donc de -0.5 à +0.5 par rapport à ce nombre
		plt.xticks(np.arange(-0.5, self.x + 0.5, 1))	# La légende (et donc les lignes de la grille) vont de -0.5 à X + 0.5
		plt.yticks(np.arange(-0.5, self.y + 0.5, 1))	# La légende (et donc les lignes de la grille) vont de -0.5 à Y + 0.5
		fig.tight_layout()
		plt.show()

	##################################################
	def draw_on_fig(self, fig, canvas):
		"""Dessine le tableau avec matplotlib dans une figure et un canvas preexistant."""
		fig.clf()  # Efface le contenu de la figure existante
		ax = fig.add_subplot(111)
		ax.imshow(self.space[:,::-1].T, cmap="gray_r")
		ax.grid(color='lightblue', linestyle='-', linewidth=0.5) 
		ax.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)
		ax.set_xticks(np.arange(-0.5, self.x + 0.5, 1)) 
		ax.set_yticks(np.arange(-0.5, self.y + 0.5, 1))
		fig.tight_layout()
		canvas.draw()  # Redessine la figure


	##################################################
	def random_seed(self, x = 80, y = 45):
		"""
		Creation d'une grille aleatoire de taille x et y mais en forcant une distribution de 20% d'elements en vie.
		
			Parametres:
				x (int): Taille en largeur de la grille (par defaut : 80)
				y (int): Taille en Hauteur de la grille (par defaut : 45)
		"""
		# Graine Aléatoire 
		self.x = x
		self.y = y
		self.space = np.random.choice([False, True], size=(self.x, self.y), p=[0.8, 0.2])
	
	##################################################
	def white_seed(self, x = 80, y = 45):
		"""
		Creation d'une grille vide de taille x et y.
		
			Parametres:
				x (int): Taille en largeur de la grille (par defaut : 80)
				y (int): Taille en Hauteur de la grille (par defaut : 45)
		"""
		# Graine Aléatoire 
		self.x = x
		self.y = y
		self.space = np.full((self.x, self.y), False, dtype=bool)

# Tests
#r = LifeSimulator()
#print(LifeSimulator.__doc__)
#print(LifeSimulator.load.__doc__)
#print(LifeSimulator.update.__doc__)
#print(LifeSimulator.draw.__doc__)
#print(LifeSimulator.random_seed.__doc__)
#r.draw()
#r.update()
#r.draw()

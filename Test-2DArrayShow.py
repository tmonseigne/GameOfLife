# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt

X = 80
Y = 45

# Initialisation du tableau de booléens aléatoires mais en forçant une distribution de 80% de false et 20% de true
tableau = np.random.choice([False, True], size=(X, Y), p=[0.8, 0.2])

# Affichage de la grille avec Matplotlib
fig = plt.figure(figsize=(16,9),dpi=120)    
# tableau[:,::-1].T			Transpose pour avoir les x sur l'axe des abscisses sur notre dessin et on inverse l'axe des ordonnées
plt.imshow(tableau[:,::-1].T, cmap="gray_r")									# Affiche notre tableau comme une image
plt.grid(color='lightblue', linestyle='-', linewidth=0.5)						# Affichage de la grille
plt.tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)	# Supprime les légendes sur X et Y
# La légende (et donc les lignes de la grille) vont de -0.5 à MAX + 0.5 en allant de 1 en 1
# On a 0.5 de décallage car chaque cas de notre tableau est centré sur un nombre entier et sa visualisation va donc de -0.5 à +0.5 par rapport à ce nombre
plt.xticks(np.arange(-0.5, X + 0.5, 1))	# La légende (et donc les lignes de la grille) vont de -0.5 à X + 0.5
plt.yticks(np.arange(-0.5, Y + 0.5, 1))	# La légende (et donc les lignes de la grille) vont de -0.5 à Y + 0.5

fig.tight_layout()
 
plt.show()
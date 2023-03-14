# -*- coding: utf-8 -*-
import sys
import matplotlib.pyplot as plt
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QAction, QApplication, QSizePolicy, QVBoxLayout, QWidget, QFileDialog
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class MainWindow(QMainWindow):
	def __init__(self):
		"""Création de la fenêtre QT (avec un graphique à l'intérieur)"""
		super().__init__()

		# Titre de la fenêtre
		self.setWindowTitle("Jeu de la vie")

		# Définition de la taille de la fenêtre
		self.setGeometry(100, 100, 800, 600)

		# Définition du menu "Fichier"
		main_menu = self.menuBar()
		file_menu = main_menu.addMenu("Fichier")

		# Ajout de l'option "Ouvrir" au menu "Fichier"
		open_action = QAction("Ouvrir", self)
		open_action.triggered.connect(self.open_file)
		file_menu.addAction(open_action)
	
		# Ajout de l'option "Quitter" au menu "Fichier"
		exit_action = QAction("Quitter", self)
		exit_action.triggered.connect(self.close)
		file_menu.addAction(exit_action)

		# Ajout de l'option "Aide" au menu "Aide"
		help_action = QAction("?", self)
		help_action.triggered.connect(self.show_help)
		main_menu.addAction(help_action)

		# Création d'un widget pour contenir le graphique Matplotlib
		self.plot_widget = QWidget(self)
		self.setCentralWidget(self.plot_widget)

		# Définition du graphique Matplotlib
		self.fig = Figure(figsize=(5, 4), dpi=100)
		self.canvas = FigureCanvas(self.fig)
		layout = QVBoxLayout(self.plot_widget)
		layout.addWidget(self.canvas)

		# Définition des boutons "Start" et "Stop"
		self.start_button = QtWidgets.QPushButton('Start', self)
		self.start_button.clicked.connect(self.start_animation)
		self.stop_button = QtWidgets.QPushButton('Stop', self)
		self.stop_button.clicked.connect(self.stop_animation)

		# Ajout des boutons au widget principal
		button_layout = QtWidgets.QHBoxLayout()
		button_layout.addWidget(self.start_button)
		button_layout.addWidget(self.stop_button)
		layout.addLayout(button_layout)

		# Initialisation des données pour le graphique
		self.x = np.arange(0, 2 * np.pi, 0.01)
		self.y = np.sin(self.x)

		# Création de la courbe sur le graphique
		self.line, = self.fig.add_subplot(111).plot(self.x, self.y)

		# Initialisation des variables d'animation
		self.animation_running = False
		self.timer = None

	##### Menu #####
	def open_file(self):
		"""Ouvre un fichier texte et l'affiche sur le graphique"""

		# Ouvre une boîte de dialogue pour sélectionner un fichier
		file_path, _ = QFileDialog.getOpenFileName(self, "Ouvrir un fichier", "", "Fichiers texte (*.txt)")

		# Vérifie si l'utilisateur a sélectionné un fichier
		if file_path:
			# Charge les données du fichier
			with open(file_path, "r") as file:
				data = file.read().splitlines()
				print(data)

			# Met à jour les données du graphique
			# .....

	def show_help(self):
		"""Affiche une pop-up d'aide"""
		QtWidgets.QMessageBox.about(self, "Aide", "Voici la pop up avec le blabla traditionnel en version non traditionnel.")

	##### Affichage #####

	def start_animation(self):
		"""Démarre l'animation du graphique"""
		self.animation_running = True
		self.timer = self.canvas.new_timer(100, [(self.update_graph, (), {})])
		self.timer.start()

	def stop_animation(self):
		"""Arrête l'animation du graphique"""
		self.animation_running = False
		if self.timer is not None:
			self.timer.stop()

	def update_graph(self):
		"""Met à jour la courbe sur le graphique"""
		self.x += 0.1
		self.y = np.sin(self.x)
		self.line.set_data(self.x, self.y)
		self.canvas.draw()

if __name__ == '__main__':
	app = QApplication(sys.argv)
	window = MainWindow()
	window.show()
	sys.exit(app.exec_())
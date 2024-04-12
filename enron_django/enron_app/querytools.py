"""
Ce script contient des fonctions destinées à être utilisées après des requêtes de l'utilisateur.
Il est inclu dans views.py.

Au programme :
"""

def MailThresholdOnPeriod(period, threshold, type, internalOnly):
	"""Détermine les employés qui ont envoyé et/ou reçu plus que (resp. moins que)
	x mails dans un intervalle de temps choisi, avec possibilité de faire la différence 
	entre échanges internes et/ou internes-externes.

	:param period: time ; période de temps étudiée
	:param threshold: int ; seuil de mails (le 'x' ci-dessus)
	:param type: char ;  receveur 'r'(receiver), envoyeur 's'(sender) ou les deux 'a'(any)
	:param internalOnly: bool ;  considère seulement les adresses internes (@enron) si TRUE
	:return: list ; employés vérifiant les critères de recherche.
	"""

def ContentExtractor(message):
	"""
	Récupère le contenu du mail référencé par l'instance message
	:param message: instance de models.Message ; le message ciblé
	:return: string ; le contenu du mail
	"""
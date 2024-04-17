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

"""
-- combien de mails envoyés par les addresses des employés ? Sur telle période de temps ?
select e.id as employee, a.address, count(m.id)
from enron_app_employee e, enron_app_message m, enron_app_mailaddress a, enron_app_employeetomailaddress j
where m.sender_id = a.id and a.id = j.mailaddress_id and e.id = j.employee_id
and m.date between '2000-07-01'and'2000-08-01' 
group by e.id, a.address
order by e.id;

"""
def ContentExtractor(message):
	"""
	Récupère le contenu du mail référencé par l'instance message
	:param message: instance de models.Message ; le message ciblé
	:return: string ; le contenu du mail
	"""
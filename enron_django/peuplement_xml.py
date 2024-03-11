from enron_app.models import *
import xml.etree.ElementTree as ET

XML_PATH = "/Users/thibautgipteau/M1DS/SEMESTRE 2/Bases de Données/ProjetBDDR/Ressources/employes_enron.xml"

tree = ET.parse(XML_PATH)
root = tree.getroot()

""" MICRO TUTO XMLPARSER

root.tag	->	"Employees"
root[22]	->	<employé 23>
root[2].attrib	->	"{'category': 'Employee'}"

root[0][2].attrib['address']	->	"marie.heard@enron.com"

root[2][0].tag	->	"lastname"
root[2][0].text	-> "Donoho"

"""

"""for employee in root :
	if len(employee.attrib) > 0 :
		print(f"category = {employee.attrib['category']}")
	else :
		print(f"category = N/A")
	for ligne in employee :
		if ligne.tag == 'email' :
			print(f"email = {ligne.attrib['address']}")

		else :
			print(f"{ligne.tag} = {ligne.text}")

	print('------------------\n')
"""

for employee in root :

	e = Employee()
	mails = []
	employeetomail = []

	if len(employee.attrib) > 0 :
		e.category = employee.attrib['category']
	else :
		e.category = None

	for ligne in employee :

		if ligne.tag == 'email' :

			mail = MailAdress()
			mail.address = ligne.attrib['address']
			mails.append(mail)

		elif ligne.tag == 'lastname' :
			e.nom = ligne.text

		elif ligne.tag == 'firstname' :
			e.prenom = ligne.text

		elif ligne.tag == 'mailbox' :
			e.mailbox = ligne.text

	e.save()
	for mail in mails :
		etom = EmployeetoMailadress()
		mail.save()
		etom.employee_id = e
		etom.mailadress_id = mail
		etom.save()




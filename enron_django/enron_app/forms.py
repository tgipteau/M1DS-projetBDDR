from django import forms
from .models import *


class EmployeeModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.prenom+" "+obj.nom


class AddressModelChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.address


class Basic_mining_form(forms.Form):

	fromDate = forms.DateField(help_text="From date : ")
	toDate = forms.DateField(help_text="To date : ")

	CHOIXTYPE = [
		(1, 'Internes (reçus par internes seulement)'),
		(2, 'Externes (reçus par des externes)'),
		(3, 'Indifférent')
	]
	type = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=CHOIXTYPE,
		initial=None
	)

	sentBy = forms.CharField(max_length=50, required=False)
	otherSentBy = forms.CharField(max_length=50, required=False)
	subjectContains = forms.CharField(max_length=50, required=False)


class Seuils_form(forms.Form):
	fromDate = forms.DateField()
	toDate = forms.DateField()

	CHOIXENVOUREC = [
		(1, 'Envoyés'),
		(2, 'Reçus'),
	]
	envOuRec = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=CHOIXENVOUREC,
		initial=None
	)

	CHOIXTYPE = [
		(1, 'Internes (reçus par internes seulement)'),
		(2, 'Indifférent'),
		(3, 'Externes (reçus par des externes)')
	]
	type = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=CHOIXTYPE,
		initial=None
	)


class Interactions_form(forms.Form):
	fromDate = forms.DateField()
	toDate = forms.DateField()
	seuil = forms.IntegerField()

	focusOption = forms.BooleanField(initial=False, required=False)
	focusOn = forms.CharField(max_length=50, initial='Dasovich', required=False)


class Achalandage_form(forms.Form):

   fromDate = forms.DateField()
   toDate = forms.DateField()

   CHOIXTYPE = [
		(1, 'Internes / internes'),
		(2, 'Internes / Externes+Internes'),
		(3, 'Indifférent'),
	]
   type = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=CHOIXTYPE,
		initial=None
	)

   CHOIXBULKBY = [
		(1, 'Jours'),
		(2, 'Quinzaine')
	]
   bulkBy = forms.ChoiceField(
		widget=forms.RadioSelect,
		choices=CHOIXBULKBY,
		initial=None
   )


class Mailmatcher_form(forms.Form):

    employees = EmployeeModelChoiceField(queryset=Employee.objects.all())

    query = MailAddress.objects.filter(internal=True).order_by('address')
    mail_address = AddressModelChoiceField(queryset=query)

from django import forms

class Threshold_sort_form(forms.Form):

   fromDate = forms.DateField(help_text="From date : ")
   toDate = forms.DateField(help_text="To date : ")

   CHOIX =  [
      (1, 'Internes'),
      (2, 'Externes'),
      (3, 'Internes+Externes')
   ]
   type = forms.ChoiceField(
      widget=forms.RadioSelect,
      choices=CHOIX,
      initial=None
   )

   sentBy = forms.CharField(max_length= 50, help_text="Sent by address : ", required=False)







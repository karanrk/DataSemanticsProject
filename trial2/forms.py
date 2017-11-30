from django import forms
from trial2.models import MyPost

class hform(forms.ModelForm):

	disease = forms.CharField()

	# address = forms.CharField()

	ShowSymptom = forms.BooleanField(required=False)

	NearestPrimaryDoctor = forms.BooleanField(required=False)

	NearestSecondaryDoctor = forms.BooleanField(required=False)

	EstimatedCost = forms.BooleanField(required=False)


	class Meta:
		model = MyPost 
		fields = ('disease','ShowSymptom','NearestPrimaryDoctor','NearestSecondaryDoctor','EstimatedCost') 

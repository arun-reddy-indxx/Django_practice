from django import forms

class CreateNewList(forms.Form):
    name= forms.CharField(label="Name",max_length=200)
    check=forms.BooleanField(required=False)

class UploadFileForm(forms.Form):
    excel_file = forms.FileField(label='Upload Excel file')
    number = forms.IntegerField(label='Enter the Revenue Cap')
    string_input = forms.CharField(label='Enter the Leve1 classification', max_length=100)

    
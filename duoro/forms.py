from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField(max_length=254)
    company = forms.CharField(max_length=160, required=False)
    details = forms.CharField(widget=forms.Textarea, max_length=4000)
    website = forms.CharField(required=False)

    def clean_website(self):
        value = self.cleaned_data.get("website", "")

        if value:
            raise forms.ValidationError("Invalid submission.")

        return value

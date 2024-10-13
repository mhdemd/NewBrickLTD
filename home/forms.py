from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label="Your Name",
        max_length=255,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Your Name", "class": "form-control"}
        ),
    )
    phone = forms.CharField(
        label="Phone No.",
        max_length=20,
        required=True,
        widget=forms.TextInput(
            attrs={"placeholder": "Phone No.", "class": "form-control"}
        ),
    )
    email = forms.EmailField(
        label="Email Address",
        required=True,
        widget=forms.EmailInput(
            attrs={"placeholder": "Email Address", "class": "form-control"}
        ),
    )
    message = forms.CharField(
        label="Message",
        required=True,
        widget=forms.Textarea(
            attrs={
                "placeholder": "Message",
                "class": "form-control",
                "maxlength": "500",
            }
        ),
        max_length=800,
    )

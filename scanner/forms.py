from django import forms


class ScanForm(forms.Form):
    url = forms.URLField(
        label="Website URL",
        max_length=2048,
        widget=forms.URLInput(attrs={
            "placeholder": "https://example.com",
            "class": "url-input",
        }),
    )

    def clean_url(self):
        url = self.cleaned_data["url"].strip()

        if not url.lower().startswith("https://"):
            raise forms.ValidationError(
                "Please enter an HTTPS URL."
            )

        return url

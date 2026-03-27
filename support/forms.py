from django import forms


class SupportForm(forms.Form):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors",
            "placeholder": "your.email@example.com",
        })
    )

    request_type = forms.ChoiceField(
        choices=[
            ("", "Select a request type"),
            ("cancel-subscription", "Cancel subscription"),
            ("refund-recent-charge", "Refund recent charge"),
            ("other", "Other"),
        ],
        widget=forms.Select(attrs={
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors",
        })
    )

    message = forms.CharField(
        widget=forms.Textarea(attrs={
            "rows": 6,
            "class": "w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-green-500 focus:border-green-500 transition-colors resize-vertical",
            "placeholder": "Please describe your issue or question in detail...",
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        return cleaned_data

from django import forms


class ContactForm(forms.Form):
    """
    Form for handling contact requests from users.

    Includes name, email, subject, and message fields with appropriate
    validation and styling.
    """

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Your name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Your email",
            }
        )
    )

    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Message subject",
            }
        ),
    )

    message = forms.CharField(
        widget=forms.Textarea(
            attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Your message",
                "rows": 5,
            }
        )
    )


class NewsletterForm(forms.Form):
    """
    Form for newsletter subscription.

    Simple form with just an email field for newsletter subscriptions.
    """

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Your email",
            }
        )
    )

from django import forms
from django.utils import timezone
from .models import Case


class ProofLinkForm(forms.ModelForm):
    class Meta:
        model = Case
        fields = ["proof_link"]

    def clean(self):
        cleaned_data = super().clean()

        # Only allow proof submission when case is PROCESSING
        if self.instance.status != "PROCESSING":
            raise forms.ValidationError(
                "Proof can only be submitted when the case is in PROCESSING status."
            )

        return cleaned_data

    def save(self, commit=True):
        case = super().save(commit=False)

        # Switch to review stage
        case.status = "AWAITING_REVIEW"
        case.proof_submitted_at = timezone.now()

        if commit:
            case.save()

        return case
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect

from .models import Case
from .forms import ProofLinkForm


def case_list(request):
    cases = Case.objects.select_related("shelter").order_by("-created_at")
    return render(request, "cases/case_list.html", {"cases": cases})


def case_detail(request, pk):
    case = get_object_or_404(Case.objects.select_related("shelter"), pk=pk)

    can_submit_proof = (
        case.status == "PROCESSING"
        and request.user.is_authenticated
        and case.shelter.owner_id == request.user.id
    )

    proof_form = ProofLinkForm(instance=case) if can_submit_proof else None

    if request.method == "POST" and "submit_proof" in request.POST:
        if not can_submit_proof:
            messages.error(request, "Only the shelter owner can submit proof for this case.")
            return redirect("cases:detail", pk=case.pk)

        proof_form = ProofLinkForm(request.POST, instance=case)
        if proof_form.is_valid():
            proof_form.save()
            messages.success(request, "Proof link submitted. Case is now awaiting admin review.")
            return redirect("cases:detail", pk=case.pk)

    return render(
        request,
        "cases/case_detail.html",
        {
            "case": case,
            "proof_form": proof_form,
            "can_submit_proof": can_submit_proof,
        },
    )
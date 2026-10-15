from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.shortcuts import render
from .forms import ScanForm
from .services import scan_website
from django.contrib.auth.decorators import login_required



@login_required
def home(request):
    form = ScanForm()
    result = None
    submitted_url = ""

    if request.method == "POST":
        form = ScanForm(request.POST)
        if form.is_valid():
            submitted_url = form.cleaned_data["url"]
            result = scan_website(submitted_url)

    return render(
        request,
        "scanner/index.html",
        {
            "form": form,
            "result": result,
            "submitted_url": submitted_url,
        },
    )
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserCreationForm()

    return render(request, "registration/register.html", {"form": form})

from django.shortcuts import render, redirect

from cakery.forms import CakeForm
from cakery.models import Baker, Cake


# Create your views here.
def index(request):
    cakes = Cake.objects.all()
    return render(request, 'index.html', context={'cakes': cakes})

def add_cake(request):
    baker = Baker.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.baker = Baker.objects.filter(user=request.user).first()
            cake.save()

        return redirect('index')

    form = CakeForm()
    return render(request, 'add-cake.html', context={'form': form, 'baker': baker})
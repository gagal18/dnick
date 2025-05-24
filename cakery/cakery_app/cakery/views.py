from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect

from cakery.forms import CakeForm
from cakery.models import Baker, Cake


def index(request):
    cakes = Cake.objects.all()
    return render(request, 'index.html', context={'cakes': cakes})


def add_cake(request):
    baker = Baker.objects.filter(user=request.user).first() if request.user.is_authenticated else None
    if not baker:
        return render(request, 'add-cake.html', {
            'form': CakeForm(),
            'baker': None,
            'error': "Baker not found for current user."
        })

    if request.method == 'POST':
        form = CakeForm(request.POST, request.FILES)
        if form.is_valid():
            cake = form.save(commit=False)
            cake.baker = baker
            obj = cake

            baker_cakes = Cake.objects.filter(baker=baker)
            baker_cakes_count = baker_cakes.count()

            if baker_cakes_count == 10:
                form.add_error(None, "You can't have more than 10 cakes.")
            else:
                total_price = sum(c.price for c in baker_cakes)
                if total_price + obj.price > 10000:
                    form.add_error(None, "Total cake price exceeds 10,000.")
                elif Cake.objects.exclude(pk=obj.pk).filter(name=obj.name).exists():
                    form.add_error('name', "A cake with this name already exists.")
                else:
                    try:
                        cake.full_clean()
                        cake.save()
                        return redirect('index')
                    except ValidationError as e:
                        for field, errors in e.message_dict.items():
                            for error in errors:
                                form.add_error(field, error)

    else:
        form = CakeForm()

    return render(request, 'add-cake.html', context={'form': form, 'baker': baker})

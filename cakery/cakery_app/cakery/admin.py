from django.contrib import admin

from cakery.models import Cake, Baker

class CakeAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return obj and obj.baker.user == request.user
    def has_view_permission(self, request, obj = ...):
        return True
    def save_model(self, request, obj, form, change):
        baker = Baker.objects.get(user=request.user)
        baker_cakes = Cake.objects.filter(baker=baker).all()
        if Cake.objects.filter(name=obj.name).exists():
            return

        if not change and baker_cakes.count() == 10:
            return
        sum_cakes = sum(cake.price for cake in baker_cakes)
        print(sum_cakes)
        cake_current = Cake.objects.get(id=obj.id)
        if not change and sum_cakes + obj.sum > 10000:
            return
        if change and sum_cakes + obj.sum - cake_current.price > 10000:
            return

        super(CakeAdmin, self).save_model(request, obj, form, change)



class BakerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)
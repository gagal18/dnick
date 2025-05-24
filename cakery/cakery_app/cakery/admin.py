from django.contrib import admin

from cakery.models import Cake, Baker


class CakeAdmin(admin.ModelAdmin):
    def has_change_permission(self, request, obj=None):
        return obj and obj.baker.user == request.user

    def has_view_permission(self, request, obj=None):
        return True

    def save_model(self, request, obj, form, change):
        baker = Baker.objects.filter(user=request.user).first()
        if not baker:
           return

        baker_cakes = Cake.objects.filter(baker=baker)
        baker_cakes_count = baker_cakes.count()

        if not change and baker_cakes_count == 10:
            return
        total_price = sum(cake.price for cake in baker_cakes)
        old_cake = baker_cakes.filter(id=obj.id).first()

        if not change and total_price + obj.price > 10000:
            return
        if change and old_cake and total_price + obj.price - old_cake.price > 10000:
            return
        if Cake.objects.exclude(pk=obj.pk).filter(name=obj.name).exists():
            return
        obj.baker = baker
        super().save_model(request, obj, form, change)

class BakerAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(Cake, CakeAdmin)
admin.site.register(Baker, BakerAdmin)
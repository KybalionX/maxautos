from django.contrib import admin
from maxapp.models import Coche, Imagen
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import ugettext, ugettext_lazy as _
from copy import deepcopy
from django.utils.safestring import mark_safe


from rest_framework.response import Response
admin.site.unregister(User)

# Register your models here.

class CocheImagenAdmin(admin.StackedInline):
    model = Imagen
    min_num = 1
    max_num = 5
    extra = 1

    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        # ex. the name of column is "image"
        if obj.imagen:
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format("https://maxautos.pythonanywhere.com/media/"+str(obj.imagen)))
        else:
            return '(No image)'

    image_preview.short_description = 'Preview'

    image_preview.short_description = 'Preview'

@admin.register(Coche)
class CocheAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'placa',
        'marca',
        'modelo',
        'cantidad',
        'precio'
    ]
    list_display_links = ['id','placa']

    inlines = [CocheImagenAdmin]
    search_fields = ['marca', 'modelo', 'placa']

    class Meta:
        model = Coche


@admin.register(User)
class MyUserAdmin(UserAdmin):
    model = User
    list_filter = ('is_staff','is_active','groups',)

    #Se oculta el campo "Es superusuario" para los que no son superUsuario
    def get_fieldsets(self, request, obj=None):
        fieldsets = super(UserAdmin, self).get_fieldsets(request, obj)
        if not obj:
            return fieldsets

        if not request.user.is_superuser or request.user.pk == obj.pk:
            fieldsets = deepcopy(fieldsets)
            for fieldset in fieldsets:
                if 'is_superuser' in fieldset[1]['fields']:
                    if type(fieldset[1]['fields']) == tuple :
                        fieldset[1]['fields'] = list(fieldset[1]['fields'])
                    fieldset[1]['fields'].remove('is_superuser')
                    break
        return fieldsets


    #Si el usuario no es superusuario, se oculta el superusuario para que no se pueda editar
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs



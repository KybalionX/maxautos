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
        if obj.imagen:
            
            return mark_safe('<img src="{0}" width="150" height="150" style="object-fit:contain" />'.format("https://api.probandoserver.xyz/"+str(obj.imagen)))

        else:
            return '(No tiene imagen)'


    image_preview.short_description = 'Vista Previa'

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

    #Si el usuario no es superusuario, se oculta el checkbox en las opciones de editar Usuario
    def get_fieldsets(self, request, obj=None):
        if not obj:
            return self.add_fieldsets

        if request.user.is_superuser:
            perm_fields = ('is_active', 'is_staff', 'is_superuser',
                           'groups', 'user_permissions')
        else:
            # modify these to suit the fields you want your
            # staff user to be able to edit
            perm_fields = ('is_active', 'is_staff', 'groups', 'user_permissions')

        return [(None, {'fields': ('username', 'password')}),
                (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
                (_('Permissions'), {'fields': perm_fields}),
                (_('Important dates'), {'fields': ('last_login', 'date_joined')})]


    #Si el usuario no es superusuario, se oculta el superusuario para que no se pueda editar
    def get_queryset(self, request):
        qs = super(UserAdmin, self).get_queryset(request)
        if not request.user.is_superuser:
            return qs.filter(is_superuser=False)
        return qs



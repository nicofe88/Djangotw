from django.contrib import admin
from .models import Profile, Post

class TwiterAdmin(admin.AdminSite):
    site_header='Administracion Twiter'
    site_title='Administracion SuperUser'
    index_title='Administracion'
    empty_value_display='No hay registros'

class ProfileAdmin(admin.ModelAdmin):
    list_display=('user','image')
 

# admin.site.register(Profile)
# admin.site.register(Post)

#personalizacion
sitio_admin=TwiterAdmin(name='tweterAdmin')
sitio_admin.register(Profile,ProfileAdmin)
sitio_admin.register(Post)

from django.contrib import admin
from filebrowser.sites import site

# FileBrowser URL-ni admin saytga ulash
site.directory = ''
admin.site.register_site(site)
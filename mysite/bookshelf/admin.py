from django.contrib import admin

from .models import Author, Book, Comment


class AutorModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'description', )
    list_display_links = ('name', )
    prepopulated_fields = {'slug': ('name', )}


class BookModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'author', )
    list_display_links = ('title', )
    prepopulated_fields = {'slug': ('title', )}


admin.site.register(Book, BookModelAdmin)
admin.site.register(Author, AutorModelAdmin)
admin.site.register(Comment)

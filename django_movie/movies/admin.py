from django.contrib import admin
from movies.models import *
from django.utils.safestring import mark_safe
from django import forms

from ckeditor_uploader.widgets import CKEditorUploadingWidget

# from post.models import Post

class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'url')
    list_display_links = ('name', 'id')


class ReviewInLine(admin.TabularInline):
    model = Review
    extra = 1
    readonly_fields = ('email', 'name')


class MovieShortsInline(admin.TabularInline):
    model = MovieShorts
    extra = 1

    readonly_fields = ('get_image',)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="60">')
    
    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')
    list_editable = ('draft',)
    search_fields = ('title', 'category__name')
    readonly_fields = ('get_image',)
    inlines = [MovieShortsInline, ReviewInLine]
    form = MovieAdminForm
    actions = ['publish', 'unpublish']
    save_on_top = True
    save_as = True
    # fields = (('actors', 'directors', 'genres'),)
    fieldsets = (
        (None, {
        'fields' : (('title', 'tagline'),)
        }),
        (None, {
        'fields' : ('description', ('poster', 'get_image'))
        }),
        (None, {
        'fields' : (('year', 'world_premiere'), 'country')
        }),
        ('Actors', {
        'classes' : ('collapse',),
        'fields' : (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
        'fields' : (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        (None, {
        'fields' : (('url', 'draft'),)
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="auto">')
    
    get_image.short_description = 'Изображение'

    def unpublish(self, request, queryset):
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись обновлена'
        else:
            message_bit = f'{row_update} записей обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    unpublish.short_description = 'Снять с публикации'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('email', 'name')

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')

@admin.register(Actors)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image',)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')
    
    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('movie', 'star', 'ip')

@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)

@admin.register(MovieShorts)
class MovieShortsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_image')
    readonly_fields = ('get_image',)
    
    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="70" height="60">')
    
    get_image.short_description = 'Изображение'


admin.site.site_title = 'Django Movies'
admin.site.site_header = 'Django Movies'

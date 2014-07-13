# -*- coding: utf-8 -*-

from django.contrib import admin


class PictureInline(admin.TabularInline):
    template = 'meringue/edit_inline/gallery.html'
    extra = 0

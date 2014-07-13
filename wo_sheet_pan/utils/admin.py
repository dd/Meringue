# -*- coding: utf-8 -*-

from django.contrib import admin


class PictureInline(admin.TabularInline):
    template = 'wo_sheet_pan/edit_inline/gallery.html'
    extra = 0

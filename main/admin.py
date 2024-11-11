from django.contrib import admin
from .models import *
from django import forms
from django.contrib import admin
from .models import KpiModel, WorkModel, SportModel, EvrikaModel, BookModel, DeadlineModel, MeetingModel, \
    MeetingDateModel, SportDateModel


class KPIModelForm(forms.ModelForm):
    class Meta:
        models = KpiModel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['league'].widget.attrs['readonly'] = True
        self.fields['koef'].widget.attrs['readonly'] = True


class KPIAdmin(admin.ModelAdmin):
    form = KPIModelForm
    list_display = ('name', 'general', 'league', 'koef', 'book_comment', 'upwork')


class WorkAdmin(admin.ModelAdmin):
    def kpi_users(self, obj):
        return obj.kpi.name

    def get_date(self, obj):
        return obj.deadline.date

    list_display = ("score", "kpi_users", "get_date")


class SportAdmin(admin.ModelAdmin):
    def kpi_users(self, obj):
        return obj.kpi.name

    def get_date(self, obj):
        return obj.sport_date.date

    list_display = ("score", "get_date", "kpi_users")


class SportDateModelAdmin(admin.ModelAdmin):
    list_display = ('date',)


class DeadlineModelAdmin(admin.ModelAdmin):
    list_display = ['date']


class BookModelAdmin(admin.ModelAdmin):
    def get_book_title(self, obj):
        return obj.book.title

    def kpi_users(self, obj):
        return obj.kpi.name

    list_display = ("get_book_title", "score", "kpi_users")


class BookItemAdmin(admin.ModelAdmin):
    list_display = ("title",)


class EvrikaAdmin(admin.ModelAdmin):
    list_display = ("details", "score")


class MeetingAdmin(admin.ModelAdmin):
    def kpi_user(self, obj):
        return obj.kpi.name

    def get_date(self, obj):
        return obj.meeting_date.date

    list_display = ('score', 'kpi_user', 'get_date')


class MeetingDateAdmin(admin.ModelAdmin):
    list_display = ('date',)


admin.site.register(KpiModel, KPIAdmin)
admin.site.register(WorkModel, WorkAdmin)
admin.site.register(SportModel, SportAdmin)
admin.site.register(EvrikaModel, EvrikaAdmin)
admin.site.register(BookItem, BookItemAdmin)
admin.site.register(BookModel, BookModelAdmin)
admin.site.register(MeetingModel, MeetingAdmin)
admin.site.register(MeetingDateModel, MeetingDateAdmin)
admin.site.register(DeadlineModel, DeadlineModelAdmin)
admin.site.register(SportDateModel, SportDateModelAdmin)

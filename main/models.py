from typing import Iterable, Optional
from django.db import models
from django.contrib.auth.models import User


class WorkManager(models.Manager):
    def work_sum(self, kpi):
        work = self.filter(kpi=kpi)
        return sum(float(x.score) for x in work)

class WorkModel(models.Model):
    WORK_CHOICES = (
        ("0.5", "0.5"), ("-1", "-1")
    )
    deadline = models.DateField(null=True)
    score = models.CharField(max_length=100, choices=WORK_CHOICES)
    description = models.TextField(max_length=200, null=True, blank=True)
    kpi = models.ForeignKey("KpiModel", on_delete=models.CASCADE, related_name="work_items")
    created_at = models.DateTimeField(auto_now=True)
    
    objects = WorkManager()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.kpi.calculate_general()

    def __str__(self):
        return str(self.score) + " " + str(self.deadline)

class SportManager(models.Manager):

    def sport_sum(self, kpi):
        sports = self.filter(kpi=kpi)
        return sum(x.score for x in sports)

class SportModel(models.Model):
    SPORT_CHOICES = (
        (0, 0), (-1, -1)
    )
    details = models.CharField(max_length=200)
    score = models.IntegerField(choices=SPORT_CHOICES)
    kpi = models.ForeignKey("KpiModel", on_delete=models.CASCADE, related_name="sport_items")
    created_at = models.DateTimeField(auto_now=True)
    objects = SportManager()

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.kpi.calculate_general()

    def __str__(self):
        return str(self.details) + " " + str(self.score)
    
class BooksManager(models.Manager):
    def books_sum(self, kpi):
        books = self.filter(kpi=kpi)
        return sum(x.score for x in books)


class BookItem(models.Model):
    title = models.CharField(max_length=200)
    def __str__(self):
        return self.title    
class BookModel(models.Model):
    BOOK_CHOICES = (
        (1,1), (0,0)
    )
    book = models.ForeignKey(BookItem, on_delete=models.CASCADE, related_name="book_title")
    score = models.IntegerField(null=True, choices=BOOK_CHOICES)
    kpi = models.ForeignKey("KpiModel", on_delete=models.CASCADE, related_name="book_items")
    created_at = models.DateTimeField(auto_now=True)
    objects = BooksManager()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.kpi.calculate_general()

    def __str__(self):
        return self.book.title + " " + str(self.score)
    
# Book class => title, BookScore class => book - foreignkey(Book), 
# and kpi - foreignkey(Kpi)    
    
class EvrikaManager(models.Manager):
    def evrika_sum(self, kpi):
        evrikas = self.filter(kpi=kpi)
        return sum(x.score for x in evrikas)

class EvrikaModel(models.Model):
    EVRIKA_CHOICES = (
        (5, 5), (0,0)
    )
    details = models.CharField(max_length=200)
    score = models.IntegerField(choices=EVRIKA_CHOICES)
    kpi = models.ForeignKey("KpiModel", on_delete=models.CASCADE, related_name="evrika_items")
    created_at = models.DateTimeField(auto_now=True)
    objects = EvrikaManager()
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.kpi.calculate_general()

    def __str__(self):
        return self.details + " " + str(self.score)

class KpiModel(models.Model):
    name = models.CharField(max_length=255)
    general = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, default=50)
    league = models.CharField(max_length=255, null=True, blank=True)
    koef = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    book_comment = models.URLField(max_length=255, null=True)
    upwork = models.URLField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)

    def calculate_general(self):
        book = BookModel.objects.books_sum(self)
        sport = SportModel.objects.sport_sum(self)
        work_sum = WorkModel.objects.work_sum(self)
        evrika = EvrikaModel.objects.evrika_sum(self)

        total = float(sport) + float(book) + float(evrika) + float(work_sum)
        
        if total <= 10:
            result = 50 + total
        elif total <= 23:
            result = 50 + 10 + 0.8 * (total - 10)
        elif total <= 39:
            result = 50 + 10 + 10.4 + 0.6 * (total - 23)
        elif total <= 64:
            result = 50 + 10 + 10.4 + 9.6 + 0.4 * (total - 39)
        elif total <= 114:
            result = 50 + 10 + 10.4 + 9.6 + 10 + 0.2 * (total - 64)
        elif total <= 181:
            result = 50 + 10 + 10.4 + 9.6 + 10 + 10.05 + 0.15 * (total - 114)
        elif total < 281:
            result = 50 + 10 + 10.4 + 9.6 + 10 + 10.05 + 9.95 + 0.1 * (total - 181)
        else:
            result = 50 + 10 + 10.4 + 9.6 + 10 + 10.05 + 9.95 + 10

        self.general = result


    def get_league(self):

        leagues = ['REJECTED','WOOD','STONE','BRONZE','SILVER','CRYSTAL','ELITE','LEGEND']
        return leagues[0 if self.general<40 else 7 if self.general>=110 else int(self.general//10-4)]

        # leagues = ['REJECTED','WOOD','STONE','BRONZE','SILVER','CRYSTAL','ELITE','LEGEND']
        # return leagues[0 if self.general<40 else 7 if self.general>=110 else int(self.general//10-4)]
        if self.general < 40:
            return "REJECTED"
        elif self.general < 60:
            return "WOOD"
        elif self.general < 70:
            return "STONE"
        elif self.general < 80:
            return "BRONZE"
        elif self.general < 90:
            return "SILVER"
        elif self.general < 100:
            return "CRYSTAL"
        elif self.general < 110:
            return "ELITE"
        else:
            return "LEGEND"

    def get_koef(self):
        league_pairs = {"REJECTED":1, "WOOD":1, "STONE":0.8, "BRONZE":0.6, "SILVER":0.4, "CRYSTAL":0.2, "ELITE":0.15, "LEGEND":0.1}
        league = self.get_league()
        return league_pairs[league]

    def save(self, *args, **kwargs):
        self.calculate_general()

        self.league = self.get_league()
        self.koef = self.get_koef()
        super().save(*args, **kwargs)
    
    class Meta:
        ordering = ['name', 'general', 'league', 'koef', 'book_comment', 'upwork']


    def __str__(self):
        return f"{self.name}"


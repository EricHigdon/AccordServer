from django.db import models
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

upload_storage = FileSystemStorage(location=settings.UPLOAD_URL)
FIELD_TYPES = (
    ('char', 'Text'),
    ('email', 'Email'),
    ('phone', 'Phone'),
    ('text', 'Long Text'),
    ('int', 'Number'),
    ('bool', 'Checkbox'),
    ('choice', 'Choice'),
    ('file', 'File')
)
BOOK_CHOICES = (
    ('gen', 'Genesis'),
    ('ex', 'Exodus'),
    ('lev', 'Leviticus'),
    ('num', 'Numbers'),
    ('deu', 'Deuteronomy'),
    ('joshua', 'Joshua'),
    ('judges', 'Judges'),
    ('ruth', 'Ruth'),
    ('1samuel', '1 Samuel'),
    ('2samuel', '2 Samuel'),
    ('1kings', '1 Kings'),
    ('2kings', '2 Kings'),
    ('1chronicles', '1 Chronicles'),
    ('2chronicles', '2 Chronicles'),
    ('ezra', 'Ezra'),
    ('nehimiah', 'Nehemiah'),
    ('esther', 'Esther'),
    ('job', 'Job'),
    ('psalms', 'Psalms'),
    ('proverbs', 'Proverbs'),
    ('ecclesiastes', 'Ecclesiastes'),
    ('songofsolomon', 'Song of Solomon'),
    ('isaiah', 'Isaiah'),
    ('jeremiah', 'Jeremiah'),
    ('lamentations', 'Lamentations'),
    ('ezekiel', 'Ezekiel'),
    ('daniel', 'Daniel'),
    ('hosea', 'Hosea'),
    ('joel', 'Joel'),
    ('amos', 'Amos'),
    ('obadiah', 'Obadiah'),
    ('jonah', 'Jonah'),
    ('micah', 'Micah'),
    ('nahum', 'Nahum'),
    ('habakkuk', 'Habakkuk'),
    ('zephaniah', 'Zephaniah'),
    ('haggai', 'Haggai'),
    ('zechariah', 'Zechariah'),
    ('malachi', 'Malachi'),
    ('matthew', 'Matthew'),
    ('mark', 'Mark'),
    ('luke', 'Luke'),
    ('john', 'John'),
    ('acts', 'Acts'),
    ('romans', 'Romans'),
    ('1corinthians', '1 Corinthians'),
    ('2corinthians', '2 Corinthians'),
    ('galatians', 'Galatians'),
    ('ephesians', 'Ephesians'),
    ('philippians', 'Philippians'),
    ('colossians', 'Colossians'),
    ('1thessalonians', '1 Thessalonians'),
    ('2thessalonians', '2 Thessalonians'),
    ('1timothy', '1 Timothy'),
    ('2timothy', '2 Timothy'),
    ('titus', 'Titus'),
    ('philemon', 'Philemon'),
    ('hebrews', 'Hebrews'),
    ('james', 'James'),
    ('1peter', '1 Peter'),
    ('2peter', '2 Peter'),
    ('1john', '1 John'),
    ('2john', '2 John'),
    ('3john', '3 John'),
    ('jude', 'Jude'),
    ('revelation', 'Revelation')
)
# Create your models here.

class Church(models.Model):
    admin = models.ForeignKey(User)
    slug = models.SlugField(max_length=200)
    modified_date = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.slug
    
class Page(models.Model):
    title = models.CharField(max_length=200)
    church = models.ForeignKey(Church, related_name='pages')
    template = models.TextField(max_length=5000)
    
    def __str__(self):
        return self.title
    
class Item(models.Model):
    page = models.ForeignKey(Page, related_name='items')
    title = models.CharField(max_length=200)
    image = models.FileField(storage=upload_storage, blank=True)
    content = models.TextField(max_length=5000)
    sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Form(models.Model):
    church = models.ForeignKey(Church, related_name='forms')
    name = models.CharField(max_length=200)
    recipient = models.CharField(max_length=500, help_text='a comma separated list of emails')
    
    def __str__(self):
        return self.name
    
class Field(models.Model):
    form = models.ForeignKey(Form, related_name='fields')
    name = models.CharField(max_length=200)
    field_type = models.CharField(max_length=200, choices=FIELD_TYPES)
    required = models.BooleanField()
    sort_order = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name

class Choice(models.Model):
    field = models.ForeignKey(Field, related_name='choices')
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Passage(models.Model):
    church = models.ForeignKey(Church, related_name='passages')
    book = models.CharField(max_length=200, choices=BOOK_CHOICES)
    chapter = models.IntegerField(blank=True, null=True)
    verse = models.CharField(max_length=200, blank=True)
    
    def __str__(self):
        return self.book + ' ' + str(self.chapter) + ':' + self.verse
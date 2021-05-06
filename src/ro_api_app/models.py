from django.db import models

class Author(models.Model):
    first_name = models.CharField(max_length=64, null=True, blank=True)
    middle_name = models.CharField(max_length=64, null=True, blank=True)
    last_name = models.CharField(max_length=64)
    date_of_birth = models.DateField()
    nationality = models.CharField(max_length=64)

    def __str__(self):
        author = ' '.join([self.first_name, self.middle_name, self.last_name])
        author = author.replace('  ', ' ')
        author = author.strip()
        return author


class Book(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=512)
    subtitle = models.CharField(max_length=1024, null=True, blank=True)
    year = models.DateField()
    publisher = models.CharField(max_length=256)
    isbn = models.CharField(max_length=13)

    def __str__(self):
        return self.title


class Quote(models.Model):
    text = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True)
    language = models.CharField(max_length=64)
    length_in_words = models.IntegerField(null=True, blank=True)
    editors_comment = models.TextField(null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f'[{self.author}] {self.text[:64]}{"..." if (len(self.text) > 64) else ""}'


class Tag(models.Model):
    tag = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.tag


class QuoteTag(models.Model):
    ''' Represents mappings between quotes and tags. Enables easy searching for
        quotes by tags '''

    quote = models.ForeignKey(Quote, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    def __str__(self):
        return f'[{self.tag}] {self.quote}'
from django.db import models

# Create your models here.
class Search(models.Model):
    search = models.CharField(max_length=500)
    created = models.DateTimeField(auto_now=True)

    # changing the name search.object() into actual search value
    def __str__(self):
        return '{}'.format(self.search) 

    # changing the name of search items list
    class Meta:
        verbose_name_plural = 'Searches'
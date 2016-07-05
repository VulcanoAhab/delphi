from django.db import models

# Create your models here.
class PageData(models.Model):
    '''
    '''
    field_name=models.CharField(max_length=150)
    field_value=models.TextField(null=True)
    page=models.ForeignKey('urlocators.Page')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        '''
        '''
        verbose_name_plural='Pages Data'

    def __str__(self):
        '''
        '''
        return self.field_name


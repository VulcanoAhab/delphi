from django.db import models
import hashlib

def make_control_key(field_name, value, page_id):
    '''
    '''
    control_value=':'.join([field_name, value, str(page_id)])
    hash_control=hashlib.md5()
    hash_control.update(control_value.encode())
    return hash_control.hexdigest()

# Create your models here.
class PageData(models.Model):
    '''
    '''
    control_key=models.CharField(max_length=128)
    field_name=models.CharField(max_length=150)
    field_value=models.TextField(null=True)
    page=models.ForeignKey('urlocators.Page')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    element_index=models.IntegerField(default=0)

    class Meta:
        '''
        '''
        verbose_name_plural='Pages Data'

    def __str__(self):
        '''
        '''
        return self.field_name


    def save(self, *args, **kwargs):
        '''
        '''
        if not self.control_key:
            page_id=self.page.id
            self.control_key=make_control_key(self.field_name,
                                              self.field_value,
                                              page_id)
        super().save(*args, **kwargs)

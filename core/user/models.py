from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.forms.models import model_to_dict

class User(AbstractUser):
    image = models.ImageField(upload_to='users/',null=True,blank=True)

    def get_image(self):
        if self.image:
            return '{}{}'.format(settings.MEDIA_URL, self.image)
        return '{}{}'.format(settings.STATIC_URL, 'img/empty.png')
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ['pk']

    def toJSON(self):
        item = model_to_dict(self)
        item['image'] = self.get_image()
        item['groups'] = [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        item['full_name'] = self.get_full_name()
        return item
    
    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass
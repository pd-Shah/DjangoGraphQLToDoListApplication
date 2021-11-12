from django.contrib.auth.models import User
from django.db import models
from django.utils.timezone import now

STATUS = (
    (u'in-progress', u'in-progress'),
    (u'done', u'done'),
)


class Todo(models.Model):
    title = models.CharField(max_length=256, )
    description = models.TextField(null=True, blank=True, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, )
    state = models.CharField(choices=STATUS, default=u'in-progress', max_length=256, )
    due_date = models.DateTimeField(default=now())

    def __str__(self):
        return "{0}.{1}".format(self.id, self.title)

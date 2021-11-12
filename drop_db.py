import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'DjangoGraphQLToDoListApplication.settings')
django.setup()

from django.contrib.auth.models import User

from todo.models import Todo
from faker import Faker

MAX_ITEMS = 30
faker = Faker()


def create_todo():
    for i in range(20):
        Todo.objects.create(
            title=faker.name(),
            description=faker.text(),
            user=User.objects.get(pk=faker.random_int(min=1, max=User.objects.count())),
            due_date=faker.date_time())


if __name__ == "__main__":
    create_todo()

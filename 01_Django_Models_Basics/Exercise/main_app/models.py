from django.db import models as m


class Person(m.Model):
    name = m.CharField(
        max_length=30
    )

    age = m.PositiveIntegerField()

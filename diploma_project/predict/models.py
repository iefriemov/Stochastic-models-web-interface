from django.db import models
from math import pi

class Input(models.Model):
    A = models.FloatField(
        verbose_name=' начальная ставка', default=0.5)
    b = models.FloatField(
        verbose_name=' K', default=0.2)
    w = models.FloatField(
        verbose_name=' θ', default=0.2)
    T = models.FloatField(
        verbose_name=' σ', default=0.2)
    
class Choose_Model(models.Model):
    AVAILABLE = 1
    BORROWED = 2
    ARCHIVED = 3
    STATUS = (
        (AVAILABLE, ('Модель Васичека')),
        (BORROWED, ('Модель Кокса-Ингерсолла-Росса')),
        (ARCHIVED, ('Модель Бреннана и Шварца')),
    )
    status = models.PositiveSmallIntegerField(
        choices=STATUS,
        default=AVAILABLE,
        verbose_name=' Модель'
    )
    A = models.FloatField(
        verbose_name=' начальная ставка', default=0.5)
    b = models.FloatField(
        verbose_name=' K', default=0.2)
    w = models.FloatField(
        verbose_name=' θ', default=0.2)
    T = models.FloatField(
        verbose_name=' σ', default=0.2)
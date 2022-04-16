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
    

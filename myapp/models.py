from django.db import models
from django.core.validators import RegexValidator

Phone_Validator = RegexValidator(r'^(0|0098|\+98)9(0[1-5]|[1 3]\d|2[0-2]|9[0-4]|98)\d{7}$', 'correct number format: 09123426478')

class TelegramUser(models.Model):
    user_id = models.IntegerField(unique=True)
    chat_id = models.IntegerField(unique=True)
    account_balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)  
    PhoneNumber = models.CharField(max_length=14, unique=True, blank=True, null=True, validators=[Phone_Validator])
    created_at = models.DateTimeField(auto_now=True)

class PlatformChoices(models.TextChoices):
    INSTAGRAM = 'INSTAGRAM', 'Instagram'
    TELEGRAM = 'TELEGRAM', 'Telegram'
    RUBICA = 'RUBICA', 'Rubica'

class Products(models.Model):
    Platform = models.CharField(max_length=50, choices=PlatformChoices.choices, default=PlatformChoices.INSTAGRAM)
    Price = models.IntegerField(null=False)
    Name = models.CharField(max_length=100)

    def __str__(self):
        return self.Name
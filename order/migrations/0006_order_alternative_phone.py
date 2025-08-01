# Generated by Django 5.2.1 on 2025-07-27 22:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0005_alter_address_options_alter_order_options_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="alternative_phone",
            field=models.CharField(
                blank=True,
                max_length=11,
                null=True,
                validators=[
                    django.core.validators.RegexValidator(
                        message="يجب أن يبدأ رقم الهاتف بـ 010، أو 011، أو 012، أو 015 ويتكون من 11 رقمًا.",
                        regex="^(01[0125])[0-9]{8}$",
                    )
                ],
                verbose_name="رقم الهاتف",
            ),
        ),
    ]

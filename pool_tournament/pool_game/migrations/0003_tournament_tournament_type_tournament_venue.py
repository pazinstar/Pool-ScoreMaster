# Generated by Django 5.0.3 on 2024-03-19 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pool_game', '0002_alter_player_tournament'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='tournament_type',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='tournament',
            name='venue',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
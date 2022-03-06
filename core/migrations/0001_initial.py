# Generated by Django 4.0.2 on 2022-03-06 01:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('acceso', '0002_remove_usuario_birthday'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wish',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('granted', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('uploaded_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items_add', to='acceso.usuario')),
                ('users_who_like', models.ManyToManyField(related_name='liked_whishes_granted', to='acceso.Usuario')),
            ],
        ),
    ]

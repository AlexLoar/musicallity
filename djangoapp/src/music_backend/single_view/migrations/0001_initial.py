# Generated by Django 2.2.5 on 2020-09-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contributor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250, verbose_name='Title')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Source',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=250, verbose_name='Title')),
                ('ident', models.CharField(max_length=250, verbose_name='Identifier')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Song',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(blank=True, max_length=250, verbose_name='Title')),
                ('iswc', models.CharField(blank=True, max_length=250, verbose_name='ISWC')),
                ('contributors', models.ManyToManyField(blank=True, related_name='songs', to='single_view.Contributor', verbose_name='Contributor')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
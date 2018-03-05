# Generated by Django 2.0.2 on 2018-03-05 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Admin', '0001_initial'),
        ('User', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(max_length=255)),
                ('createTime', models.DateTimeField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='User.User')),
            ],
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(max_length=50)),
                ('content', models.TextField(max_length=255)),
                ('createTime', models.DateTimeField()),
                ('admin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Admin.Administrator')),
            ],
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.TextField(max_length=15)),
                ('user_agent', models.TextField(max_length=100)),
                ('visitTime', models.DateTimeField()),
                ('user', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, to='User.User')),
            ],
        ),
    ]

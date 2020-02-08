# Generated by Django 3.0.2 on 2020-02-05 04:18

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('user_type', models.CharField(choices=[('S', 'Shelter'), ('P', 'Pet Parent')], default='S', max_length=2)),
                ('phone_number', models.CharField(blank=True, max_length=40)),
                ('street_number', models.CharField(blank=True, max_length=40)),
                ('street_name', models.CharField(blank=True, max_length=40)),
                ('city', models.CharField(blank=True, max_length=40)),
                ('state', models.CharField(blank=True, max_length=40)),
                ('zip', models.CharField(blank=True, max_length=40)),
                ('document', models.FileField(blank=True, upload_to='documents/')),
                ('profilePic', models.ImageField(blank=True, upload_to='userPics/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('availability', models.CharField(choices=[('A', 'Available'), ('NA', 'Not Available'), ('P', 'Pending'), ('AD', 'Adopted')], default='A', max_length=2)),
                ('breed', models.CharField(choices=[('B', 'Beagle'), ('BX', 'Boxers'), ('FB', 'French Bulldog'), ('GR', 'Golden Retriever'), ('GS', 'German Shepard'), ('L', 'Laborador'), ('PT', 'Pointers'), ('P', 'Poodle'), ('R', 'Rottweiler'), ('Y', 'Yorkshire Terrier'), ('A', 'Abyssinian'), ('BN', 'Bengal'), ('DR', 'Devon Rex'), ('H', 'Himalayan'), ('MC', 'Maine Coon'), ('PR', 'Persian'), ('RD', 'Ragdoll'), ('SH', 'Shorthairs'), ('S', 'Siamese'), ('SP', 'Sphynx'), ('M', 'Mixed Breed'), ('O', 'Other'), ('UN', 'Unknown')], default='B', max_length=2)),
                ('disposition', models.CharField(choices=[('C', 'Good with Children'), ('OA', 'Good with Other Animals'), ('L', 'Animal must be leashed at all times'), ('NA', 'Not Applicable')], default='N/A', max_length=2)),
                ('pet_type', models.CharField(choices=[('D', 'Dog'), ('C', 'Cat'), ('O', 'Other')], default='D', max_length=2)),
                ('sex', models.CharField(choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other/Unknown')], default='M', max_length=2)),
                ('name', models.CharField(max_length=40)),
                ('age', models.FloatField(blank=True, null=True)),
                ('status', models.CharField(blank=True, max_length=40)),
                ('description', models.CharField(blank=True, max_length=200)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=200)),
                ('photo', models.ImageField(blank=True, upload_to='photos/')),
                ('pet', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='pet.Pet')),
            ],
        ),
    ]

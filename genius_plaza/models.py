from django.db import models
from passlib.handlers import django as passlib_django


class UserManager(models.Manager):
    def get_users(self):
        return self.all().order_by('first_name', 'username')

    def get_user_by_pk(self, pk):
        try:
            instance = self.get(pk=pk)
        except User.DoesNotExist:
            return None
        return instance

    def get_user_by_username(self, username):
        try:
            instance = self.get(username=username)
        except User.DoesNotExist:
            return None
        return instance

    def get_user_by_email(self, email):
        try:
            instance = self.get(email=email)
        except User.DoesNotExist:
            return None
        return instance


class User(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    first_name = models.CharField(
        default='',
        max_length=100,
        null=False,
        blank=True,
        verbose_name='First name'
    )
    last_name = models.CharField(
        default='',
        max_length=100,
        null=False,
        blank=True,
        verbose_name='Last name'
    )
    email = models.EmailField(
        unique=True,
        max_length=150,
        null=False,
        blank=False,
        verbose_name='Email address'
    )
    username = models.CharField(
        unique=True,
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Username'
    )
    password = models.CharField(
        max_length=1024,
        null=False,
        blank=True,
        verbose_name='Password'
    )
    is_active = models.BooleanField(
        default=True,
        null=False,
        blank=False,
        verbose_name='Is active',
    )
    created = models.DateTimeField(
        auto_now_add=True,
        auto_now=False,
        editable=True,
        verbose_name='Created'
    )
    modified = models.DateTimeField(
        auto_now_add=False,
        auto_now=True,
        editable=True,
        verbose_name='Modified'
    )

    objects = UserManager()

    class Meta:
        db_table = 'genius_plaza_user'
        ordering = ['id', ]
        verbose_name_plural = 'Users'
        verbose_name = 'User'

    def __str__(self):
        if self.first_name and self.last_name:
            return '%s %s' % (self.first_name, self.last_name,)
        elif self.first_name:
            return '%s' % (self.first_name,)
        else:
            return self.username

    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)

    def encrypt_password(self, password):
        self.password = passlib_django.django_pbkdf2_sha256.encrypt(password)

    def verify_password(self, password):
        return passlib_django.django_pbkdf2_sha256.verify(password, self.password)


class Recipe(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    name = models.CharField(
        default='',
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Name'
    )
    user = models.ForeignKey(
        User,
        related_name='recipe',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        verbose_name='User'
    )
    steps = models.ManyToManyField(
        'Step',
        blank=True,
        verbose_name='Steps'
    )
    ingredients = models.ManyToManyField(
        'Ingredient',
        blank=True,
        verbose_name='Ingredients'
    )

    class Meta:
        db_table = 'genius_plaza_recipe'
        ordering = ['id', ]
        verbose_name_plural = 'Recipes'
        verbose_name = 'Recipe'

    def __str__(self):
        return self.name


class Step(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    step_text = models.CharField(
        default='',
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Step-text'
    )

    class Meta:
        db_table = 'genius_plaza_step'
        ordering = ['id', ]
        verbose_name_plural = 'Steps'
        verbose_name = 'Step'

    def __str__(self):
        return self.step_text


class Ingredient(models.Model):
    id = models.AutoField(
        primary_key=True
    )
    text = models.CharField(
        default='',
        max_length=100,
        null=False,
        blank=False,
        verbose_name='Ingredient-text'
    )

    class Meta:
        db_table = 'genius_plaza_ingredient'
        ordering = ['id', ]
        verbose_name_plural = 'Ingredients'
        verbose_name = 'Ingredient'

    def __str__(self):
        return self.text

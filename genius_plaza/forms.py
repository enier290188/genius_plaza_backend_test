from django import forms
from django.core import validators
from . import models

FIELD_FIRST_NAME = forms.CharField(
    label='First name',
    required=False,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'first_name',
        },
    ),
)
FIELD_LAST_NAME = forms.CharField(
    label='Last name',
    required=False,
    min_length=1,
    max_length=100,
    widget=forms.TextInput(
        attrs={
            'id': 'last_name',
        },
    ),
)
FIELD_EMAIL = forms.EmailField(
    label='Email address',
    required=True,
    min_length=1,
    max_length=150,
    widget=forms.EmailInput(
        attrs={
            'id': 'email',
        },
    ),
)
FIELD_USERNAME = forms.CharField(
    label='Username',
    required=True,
    min_length=1,
    max_length=100,
    validators=[
        validators.RegexValidator('^[a-z0-9_]+$', message='Letters, digits and _ only.'),
    ],
    widget=forms.TextInput(
        attrs={
            'id': 'username',
        },
    ),
)
FIELD_PASSWORD = forms.CharField(
    label='Password',
    required=True,
    min_length=3,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password',
        },
        render_value=False,
    ),
    strip=False,
)
FIELD_PASSWORD_CONFIRMATION = forms.CharField(
    label='Password (confirmation)',
    required=True,
    min_length=3,
    max_length=32,
    widget=forms.PasswordInput(
        attrs={
            'id': 'password_confirmation',
        },
        render_value=False,
    ),
    strip=False,
    help_text='Enter the same password as before, for verification.',
)


class FieldPasswordHashReadOnlyWidget(forms.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        print('************', name)
        result = str(value).split('$')
        if len(result) != 4:
            return 'Invalid password format or unknown hashing algorithm.'
        else:
            return '''
            <b>algorithm:</b> %s 
            <b>iterations:</b> %s 
            <b>salt:</b> %s****** 
            <b>hash:</b> %s**************************************
            ''' % (result[0], result[1], result[2][0:6], result[3][0:6])


FIELD_PASSWORD_HASH_READ_ONLY = forms.CharField(
    label='Password',
    required=False,
    widget=FieldPasswordHashReadOnlyWidget,
    help_text='Raw passwords are not stored, so there is no way to see this user\'s password, but you can change the password using <a href=\"../password/change/\">this form</a>.',
)
FIELD_IS_ACTIVE = forms.BooleanField(
    label='Is active',
    required=True,
    widget=forms.CheckboxInput(
        attrs={
            'id': 'is_active',
        },
    ),
    help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.',
)


class UserAdd(forms.ModelForm):
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    email = FIELD_EMAIL
    username = FIELD_USERNAME
    password = FIELD_PASSWORD
    password_confirmation = FIELD_PASSWORD_CONFIRMATION
    is_active = FIELD_IS_ACTIVE

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'username', 'password', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('first_name').widget.attrs.update({'autofocus': True})
        self.fields['is_active'].initial = True

    def clean(self):
        super_clean = super(UserAdd, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            # self.add_error('password', 'The password and your confirmation do not match.')
            self.add_error('password_confirmation', 'The password and your confirmation do not match.')
        return super_clean

    def save(self, commit=True):
        user = super(UserAdd, self).save(commit=False)
        # password
        password = self.cleaned_data.get('password')
        user.encrypt_password(password=password)
        if commit:
            # save to data base
            user.save()
        return user


class UserChange(forms.ModelForm):
    first_name = FIELD_FIRST_NAME
    last_name = FIELD_LAST_NAME
    email = FIELD_EMAIL
    username = FIELD_USERNAME
    password = FIELD_PASSWORD_HASH_READ_ONLY
    is_active = FIELD_IS_ACTIVE

    class Meta:
        model = models.User
        fields = ('first_name', 'last_name', 'email', 'username', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields.get('first_name').widget.attrs.update({'autofocus': True})

    def clean_password(self):
        # Regardless of what the user provides, return the initial value. This is done here, rather than on the field, because the field does not have access to the initial value.
        return self.initial['password']


class UserPasswordChange(forms.Form):
    password = FIELD_PASSWORD
    password_confirmation = FIELD_PASSWORD_CONFIRMATION

    class Meta:
        model = models.User
        fields = ('password',)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(UserPasswordChange, self).__init__(*args, **kwargs)
        self.fields.get('password').widget.attrs.update({'autofocus': True})

    def clean(self):
        super_clean = super(UserPasswordChange, self).clean()
        # password and password_confirmation
        password = self.cleaned_data.get('password')
        password_confirmation = self.cleaned_data.get('password_confirmation')
        if password != password_confirmation:
            # self.add_error('password', 'The password and your confirmation do not match.')
            self.add_error('password_confirmation', 'The password and your confirmation do not match.')
        return super_clean

    def save(self, commit=True):
        # password
        password = self.cleaned_data.get('password')
        self.user.encrypt_password(password=password)
        if commit:
            self.user.save()
        return self.user

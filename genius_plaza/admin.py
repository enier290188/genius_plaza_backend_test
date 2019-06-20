from django.contrib import admin, messages
from django.conf.urls import url
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth.models import User as AuthUser, Group as AuthGroup
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.safestring import mark_safe
from . import forms
from . import models

admin.site.unregister(AuthUser)
admin.site.unregister(AuthGroup)
admin.site.site_title = 'Genius Plaza Backend Test'
admin.site.site_header = 'Genius Plaza Backend Test'
# admin.site.site_url = 'http://www.genius-plaza-backend-test.com'
admin.site.index_title = 'Site administration'


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('list_display_full_name', 'username', 'email', 'list_display_password', 'created', 'modified', 'is_active')
    list_display_links = ('list_display_full_name', 'username', 'email')
    list_per_page = 10
    list_filter = ('is_active', 'created', 'modified')
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    ordering = ('first_name', 'last_name')
    search_fields = ('first_name', 'last_name', 'username', 'email')
    readonly_fields = ('created', 'modified')

    def list_display_full_name(self, obj):
        return '%s %s' % (obj.first_name, obj.last_name)

    def list_display_password(self, obj):
        return '%s.....' % (obj.password[0:15],)

    list_display_full_name.short_description = 'FULL NAME'
    list_display_password.short_description = 'PASSWORD'

    # fields = ('first_name', 'last_name', 'email', 'username', 'password', 'is_active', 'created', 'modified')
    fieldsets_user_add = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('User', {
            'fields': ('username', 'password', 'password_confirmation', 'is_active')
        })
    )
    fieldsets_user_change = (
        ('Personal info', {
            'fields': ('first_name', 'last_name', 'email')
        }),
        ('User', {
            'fields': ('username', 'password', 'is_active')
        }),
        ('Important dates', {
            'fields': ('created', 'modified')
        })
    )
    form_user_add = forms.UserAdd
    form_user_change = forms.UserChange
    form_user_password_change = forms.UserPasswordChange

    def get_fieldsets(self, request, obj=None):
        if obj is None:
            return self.fieldsets_user_add
        else:
            return self.fieldsets_user_change

    def get_form(self, request, obj=None, **kwargs):
        defaults = {}
        if obj is None:
            defaults['form'] = self.form_user_add
        else:
            defaults['form'] = self.form_user_change
        defaults.update(kwargs)
        return super(UserAdmin, self).get_form(request, obj, **defaults)

    def get_urls(self):
        return [url(r'^(.+)/password/change/$', self.admin_site.admin_view(self.user_password_change), name='genius_plaza_user_password_change')] + super(UserAdmin, self).get_urls()

    def user_password_change(self, request, pk, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(pk))
        if user is None:
            raise Http404('%(name)s object with primary key %(key)r does not exist.' % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(pk),
            })
        if request.method == 'POST':
            form = self.form_user_password_change(user, request.POST)
            if form.is_valid():
                form.save()
                self.log_change(request, user, 'Changed password.')
                msg = 'Password changed successfully.'
                messages.success(request, msg)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.form_user_password_change(user)
        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})
        context = {
            'title': 'Change password: %s' % escape(user),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        # Include common variables for rendering the admin template.
        context.update(self.admin_site.each_context(request))
        return TemplateResponse(
            request,
            'admin/genius_plaza/user/password_change.html',
            context
        )


@admin.register(models.Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('name', 'list_display_user', 'list_display_steps', 'list_display_ingredients')
    list_display_links = ('name',)
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    ordering = ('name',)
    search_fields = ('name',)
    # raw_id_fields = ('user',)
    filter_horizontal = ('steps', 'ingredients')

    def list_display_user(self, obj):
        if obj.user is None:
            return '-'
        else:
            return obj.user

    def list_display_steps(self, obj):
        data = [str(q) for q in obj.steps.all()]
        if len(data) == 0:
            return '-'
        return mark_safe('</br>'.join(data))

    def list_display_ingredients(self, obj):
        data = [str(q) for q in obj.ingredients.all()]
        if len(data) == 0:
            return '-'
        return mark_safe('</br>'.join(data))

    list_display_user.short_description = 'USER'
    list_display_steps.short_description = 'STEPS'
    list_display_ingredients.short_description = 'INGREDIENTS'


@admin.register(models.Step)
class StepAdmin(admin.ModelAdmin):
    list_display = ('step_text',)
    list_display_links = ('step_text',)
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    ordering = ('step_text',)
    search_fields = ('step_text',)


@admin.register(models.Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('text',)
    list_display_links = ('text',)
    list_per_page = 10
    actions_on_top = True
    actions_on_bottom = False
    actions_selection_counter = True
    ordering = ('text',)
    search_fields = ('text',)

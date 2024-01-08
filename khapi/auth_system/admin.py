from django.contrib import admin
from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .auth_core import ApiPermissionCore
from .models import ApiGroup, ApiRole, Token


class TokenAdmin(admin.ModelAdmin):
    """
    Admin class for managing Token model in the Django admin interface.
    """

    list_display = ("user", "created_at")
    search_fields = ("user", "token", "created_at")

    @receiver(post_save, sender=Token)
    def token_post_save(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="Token"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiGroup"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))

    @receiver(post_delete, sender=Token)
    def token_post_delete(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="Token"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiGroup"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))


class ApiRoleAdmin(admin.ModelAdmin):
    """
    Admin class for managing ApiRole model in the Django admin interface.
    """

    list_display = ("name", "created_at")
    search_fields = ("name", "created_at")
    exclude = ("name",)

    @receiver(post_save, sender=ApiRole)
    def apiRole_post_save(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))

    @receiver(post_delete, sender=ApiRole)
    def apiRole_post_delete(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))


class ApiGroupAdmin(admin.ModelAdmin):
    """
    Admin class for managing ApiGroup model in the Django admin interface.
    """

    list_display = ("name", "created_at")
    search_fields = ("name", "created_at")

    @receiver(post_save, sender=ApiGroup)
    def apiGroup_post_save(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiGroup"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))

    @receiver(post_delete, sender=ApiGroup)
    def apiGroup_post_delete(sender, instance, **kwargs):
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiGroup"))
        transaction.on_commit(lambda: ApiPermissionCore(update="ApiRole"))


admin.site.register(ApiRole, ApiRoleAdmin)
admin.site.register(ApiGroup, ApiGroupAdmin)
admin.site.register(Token, TokenAdmin)

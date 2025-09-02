from django.db import models
from users.models import User

class AdminProfile(models.Model):
    """Model representing admin profile information"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile', verbose_name="Pengguna")
    full_name = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nama Lengkap")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Nomor Telepon")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departemen")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Posisi")
    is_active = models.BooleanField(default=True, verbose_name="Aktif")  # type: ignore
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Dibuat Pada")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Diperbarui Pada")
    
    def __str__(self) -> str:
        user_username = getattr(self.user, 'username', 'Unknown User')
        return f"Admin Profile: {user_username}"
    
    class Meta:
        verbose_name = "Profil Admin"
        verbose_name_plural = "Profil Admin"

from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """
    Custom User model with role-based approach
    Roles are managed through Django Groups
    """
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    @property
    def role_names(self):
        """Get all role names assigned to this user"""
        return list(self.groups.values_list('name', flat=True))  # type: ignore
    
    def has_role(self, role_name):
        """Check if user has a specific role"""
        return self.groups.filter(name=role_name).exists()  # type: ignore

class ShipOwnerProfile(models.Model):
    """
    Profile for ship owners (individual or company)
    """
    OWNER_TYPE_CHOICES = (
        ('individual', 'Individual'),
        ('company', 'Company'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='ship_owner_profile')
    owner_type = models.CharField(max_length=20, choices=OWNER_TYPE_CHOICES, default='individual')
    company_name = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nama Perusahaan")
    tax_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="NPWP")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    contact_person = models.CharField(max_length=100, blank=True, null=True, verbose_name="Kontak Person")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.owner_type == 'company' and self.company_name:
            return f"{self.company_name} (Company)"
        return f"{self.user.username} (Individual)"  # type: ignore
    
    class Meta:
        verbose_name = "Profil Pemilik Kapal"
        verbose_name_plural = "Profil Pemilik Kapal"

class CaptainProfile(models.Model):
    """
    Profile for captains
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='captain_profile')
    license_number = models.CharField(max_length=50, unique=True, verbose_name="Nomor Lisensi")
    years_of_experience = models.IntegerField(blank=True, null=True, verbose_name="Tahun Pengalaman")
    vessel_type_experience = models.TextField(blank=True, null=True, verbose_name="Pengalaman Jenis Kapal")
    certification = models.TextField(blank=True, null=True, verbose_name="Sertifikasi")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    emergency_contact = models.CharField(max_length=15, blank=True, null=True, verbose_name="Kontak Darurat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.license_number}"  # type: ignore
    
    class Meta:
        verbose_name = "Profil Nahkoda"
        verbose_name_plural = "Profil Nahkoda"

class AdminProfile(models.Model):
    """
    Profile for administrative staff
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='admin_profile')
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="ID Pegawai")
    department = models.CharField(max_length=100, blank=True, null=True, verbose_name="Departemen")
    position = models.CharField(max_length=100, blank=True, null=True, verbose_name="Jabatan")
    institution = models.CharField(max_length=200, blank=True, null=True, verbose_name="Institusi")
    address = models.TextField(blank=True, null=True, verbose_name="Alamat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.employee_id}"  # type: ignore
    
    class Meta:
        verbose_name = "Profil Admin"
        verbose_name_plural = "Profil Admin"
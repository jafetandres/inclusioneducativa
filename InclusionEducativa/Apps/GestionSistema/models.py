from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.contrib.auth.models import User


class Institucion(models.Model):
    nombre = models.CharField(max_length=50)
    tipoEstablecimiento = models.CharField(max_length=50, null=True, blank=True)
    direccion = models.CharField(max_length=50)
    telefono = models.CharField(max_length=50)

    def __str__(self):
        return "{0}".format(self.nombre)


class PersonalizadoBaseUserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    foto = models.ImageField(upload_to='img_perfil', null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    cedula = models.CharField(max_length=50)
    username = models.EmailField(unique=True)
    fechaNacimiento = models.DateField()
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    tipo_usuario = models.CharField(max_length=50, null=True, blank=True)
    USERNAME_FIELD = 'username'
    objects = PersonalizadoBaseUserManager()

    def get_full_name(self):
        return self.nombres, self.apellidos

    def get_short_name(self):
        return self.nombres


class Docente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    nivelInstrucion = models.CharField(max_length=50)
    cargo = models.CharField(max_length=50)


class Representante(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    nivelInstrucion = models.CharField(max_length=50)
    ocupacion = models.CharField(max_length=50)


class Experto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    tituloUniversitario = models.CharField(max_length=50)
    experienciaProfesional = models.CharField(max_length=50)
    experienciaAcademica = models.CharField(max_length=50)
    experienciaInvestigativa = models.CharField(max_length=50)


class Estudiante(models.Model):
    nombres = models.CharField(max_length=50, null=True, blank=True)
    apellidos = models.CharField(max_length=50, null=True, blank=True)
    cedula = models.CharField(unique=True, max_length=50, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    nivel = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)

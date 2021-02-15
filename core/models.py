import os
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
        user.tipo_usuario = 'administrador'
        user.save(using=self._db)
        return user


class Usuario(AbstractBaseUser, PermissionsMixin):
    foto = models.ImageField(upload_to='img_perfil', null=True, blank=True, default='img_perfil/default-avatar.jpg')
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    username = models.EmailField(unique=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_online = models.BooleanField(default=False, null=True, blank=True)
    tipo_usuario = models.CharField(max_length=20, null=True, blank=True)
    USERNAME_FIELD = 'username'
    objects = PersonalizadoBaseUserManager()

    def get_full_name(self):
        return self.nombres, self.apellidos

    def get_short_name(self):
        return self.nombres


class Docente(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    tituloUniversitario = models.CharField(max_length=50)
    experienciaProfesional = models.TextField()


class Representante(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)


class Experto(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    cedula = models.CharField(max_length=10, unique=True)
    tituloUniversitario = models.CharField(max_length=50)
    experienciaProfesional = models.TextField()


class Estudiante(models.Model):
    estado = models.CharField(max_length=50, null=True, blank=True, default='nuevo')
    nombres = models.CharField(max_length=50, null=True, blank=True)
    apellidos = models.CharField(max_length=50, null=True, blank=True)
    cedula = models.CharField(unique=True, max_length=10, null=True, blank=True)
    fechaNacimiento = models.DateField(null=True, blank=True)
    nivel = models.CharField(max_length=50)
    institucion = models.ForeignKey(Institucion, on_delete=models.CASCADE, null=True, blank=True)
    actividadesDocente = models.FileField(upload_to='actividades', null=True, blank=True)
    actividadesRepresentante = models.FileField(upload_to='actividades', null=True, blank=True)

    def filenameDocente(self):
        return os.path.basename(self.actividadesDocente.name)

    def filenameRepresentante(self):
        return os.path.basename(self.actividadesRepresentante.name)


class Comentario(models.Model):
    emisor = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE, null=True, blank=True)
    contenido = models.TextField(null=True, blank=True)
    timestamp = models.DateTimeField(auto_now=True, null=True, blank=True)
    receptor = models.CharField(max_length=50, null=True, blank=True)

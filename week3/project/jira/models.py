from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from project.settings import AUTH_USER_MODEL

# Create your models here
BLOCK_TYPE = [
    ('New', 0),
    ('To Do', 1),
    ('In Progress', 2),
    ('Done', 3)
]


# class UserManager(BaseUserManager):
#     def _create_user(self, email, password, **extra_fields):
#         if not email:
#             raise ValueError('The given email must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
#
#     def create_user(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', False)
#         extra_fields.setdefault('is_superuser', False)
#         return self._create_user(email, password, **extra_fields)
#
#     def create_superuser(self, email, password, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)
#
#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')
#
#         return self._create_user(email, password, **extra_fields)
#


# class User(AbstractBaseUser, PermissionsMixin):
#     username = models.CharField(max_length=150, unique=True)
#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=30, blank=True)
#     last_name = models.CharField(max_length=150, blank=True)
#     is_staff = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=False)
#
#     EMAIL_FIELD = 'email'
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     objects = UserManager()
#
#     class Meta:
#         verbose_name = 'User'
#         verbose_name_plural = 'Users'

class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
    avatar = models.CharField(u'Аватар пользователя', max_length=200)
    address = models.CharField(u'Адрес пользователя', max_length=200)
    bio = models.TextField(u'Биография пользователя', null=True, blank=True)

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __str__(self):
        return self.user.username


class Project(models.Model):
    name = models.CharField(u'Название проекта', max_length=100)
    description = models.TextField(u'Описание проекта')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        verbose_name = u'Проект'
        verbose_name_plural = u'Проекты'

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.project.name


class Block(models.Model):
    name = models.CharField(u'Название блока', max_length=100)
    type = models.CharField(u'Тип задачи', choices=BLOCK_TYPE, default='New', max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(u'Название задачи', max_length=100)
    description = models.TextField(u'Описание проекта')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executor')
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    # order = models.AutoField(primary_key=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    def __str__(self):
        return self.name


class TaskDocument(models.Model):
    document = models.FileField(u'Документ', upload_to='documents/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)


class TaskComment(models.Model):
    body = models.TextField(u'Комментарий')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Комментарий к задаче'
        verbose_name_plural = u'Комментарии к задаче'

    def __str__(self):
        return self.body



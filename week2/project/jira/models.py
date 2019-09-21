from django.db import models
from django.contrib.auth.models import User

# Create your models here
BLOCK_TYPE = [
    ('New', 0),
    ('To Do', 1),
    ('In Progress', 2),
    ('Done', 3)
]


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.CharField(u'Аватар пользователя', max_length=200)
    address = models.CharField(u'Адрес пользователя', max_length=200)
    bio = models.TextField(u'Биография пользователя', null=True, blank=True)

    class Meta:
        verbose_name = u'Профиль'
        verbose_name_plural = u'Профили'

    def __str__(self):
        return self.user


class UserManager(models.Manager):
    def create(self, username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        profile = UserProfile(user=user)
        profile.save()
        return user


class Project(models.Model):
    name = models.CharField(u'Название проекта', max_length=100)
    description = models.TextField(u'Описание проекта')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = u'Проект'
        verbose_name_plural = u'Проекты'


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Block(models.Model):
    name = models.CharField(u'Название блока', max_length=100)
    type = models.CharField(u'Тип задачи', choices=BLOCK_TYPE, default='New', max_length=30)


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

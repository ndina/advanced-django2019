from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from project.settings import AUTH_USER_MODEL

BLOCK_TYPE = [
    (0, 'New'),
    (1, 'To Do'),
    (2, 'In Progress'),
    (3, 'Done')
]


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
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

    def __str__(self):
        return self.project.name


# class Block(models.Model):
#     type = models.IntegerField(u'Тип задачи', choices=BLOCK_TYPE, default=0)
#     project = models.ForeignKey(Project, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(u'Название задачи', max_length=100)
    description = models.TextField(u'Описание задачи')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executor')
    block = models.IntegerField(u'Тип задачи', choices=BLOCK_TYPE, default=0)
    # order = models.AutoField(primary_key=True)
    order = models.IntegerField()

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    def __str__(self):
        return self.name


class TaskDocument(models.Model):
    document = models.FileField(u'Документ', upload_to='jira/documents/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)

    def __str__(self):
        return 'documents of task: {}'.format(self.task.name)


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

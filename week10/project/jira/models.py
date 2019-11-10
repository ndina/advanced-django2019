from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, AbstractUser
from project.settings import AUTH_USER_MODEL
from jira.utils import validate_extension, validate_file_size

TO_DO = 0
IN_PROGRESS = 1
DONE = 2

BLOCK_TYPE = [
    (TO_DO, 'To Do'),
    (IN_PROGRESS, 'In Progress'),
    (DONE, 'Done')
]


class User(AbstractUser):
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def save(self, *args, **kwargs):
        created = self.pk is None
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class UserProfile(models.Model):
    user = models.OneToOneField(AUTH_USER_MODEL, on_delete=models.CASCADE)
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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name='project_creator')

    class Meta:
        verbose_name = u'Проект'
        verbose_name_plural = u'Проекты'

    def __str__(self):
        return self.name


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    member = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.member.username


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(u'Название задачи', max_length=100)
    description = models.TextField(u'Описание задачи')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    executor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='executor')
    block = models.IntegerField(u'Тип задачи', choices=BLOCK_TYPE, default=TO_DO)
    order = models.IntegerField()

    def send_message_about_block_status(self):
        return 'current status block {} changed'.format(self.block)

    class Meta:
        verbose_name = u'Задача'
        verbose_name_plural = u'Задачи'

    def __str__(self):
        return self.name


class TaskDocument(models.Model):
    document = models.FileField(u'Документ', upload_to='jira/documents/', validators=[validate_file_size, validate_extension],)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='document_creator')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_document')

    def __str__(self):
        return 'documents of task: {}'.format(self.task.name)


class TaskComment(models.Model):
    body = models.TextField(u'Комментарий')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_creator')
    created_at = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_comments')

    class Meta:
        verbose_name = u'Комментарий к задаче'
        verbose_name_plural = u'Комментарии к задаче'

    def __str__(self):
        return self.body


class TaskManager(models.Model):
    def user_created_tasks(self, user):
        return self.filter(creator=user)

    def user_comments(self, user):
        return self.filter(creator=user)

    def executor_tasks(self, user):
        return self.filter(executor=user)

    def block_tasks(self, block):
        return self.filter(block=block)

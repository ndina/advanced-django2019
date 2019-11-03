from abc import ABC

from rest_framework import serializers
from .models import UserProfile, BLOCK_TYPE, User

from .models import TaskComment, Task, Project, TaskDocument, ProjectMember


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ('name', 'description', 'creator', 'creator_name')

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''


class ProjectMemberSerializer(serializers.ModelSerializer):
    project = ProjectSerializer(read_only=True)
    member = UserSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField()
    executor_name = serializers.SerializerMethodField()
    executor = UserSerializer(read_only=True)
    creator = UserSerializer(read_only=True)
    executor_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Task
        fields = '__all__'

    def get_creator_name(self, obj):
        if obj.creator is not None:
            return obj.creator.username
        return ''

    def get_executor_name(self, obj):
        if obj.executor is not None:
            return obj.executor.username
        return ''


class TaskDocumentSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskDocument
        fields = '__all__'


class TaskCommentSerializer(TaskDocumentSerializer):
    creator = UserSerializer(read_only=True)
    task = TaskSerializer(read_only=True)

    class Meta:
        model = TaskComment
        fields = ('body', 'creator', 'created_at', 'task')

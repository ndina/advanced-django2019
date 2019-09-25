from abc import ABC

from rest_framework import serializers
from .models import UserProfile, BLOCK_TYPE, User

from .models import TaskComment, Task, Project


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class ProjectSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    description = serializers.CharField()
    creator = UserSerializer

    def create(self, validated_data):
        project = Project(**validated_data)
        project.save()
        return project


class ProjectMemberSerializer(serializers.Serializer):
    project = ProjectSerializer
    user = UserSerializer


class BlockSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    type = serializers.ChoiceField(choices=BLOCK_TYPE,)
    project = ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('name', 'description', 'creator', 'executor', 'block')


class TaskDocument(serializers.Serializer):
    document = serializers.FileField()
    creator = UserSerializer
    task = TaskSerializer


class TaskCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskComment
        fields = ('body', 'creator', 'created_at', 'task')

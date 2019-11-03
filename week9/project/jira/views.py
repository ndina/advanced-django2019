import logging
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from .models import User, UserProfile, Project, ProjectMember, Task, TaskComment, TaskDocument
from .serializers import UserSerializer, ProjectSerializer, TaskSerializer, ProjectMemberSerializer, TaskDocument, \
    TaskCommentSerializer, TaskDocumentSerializer


logger = logging.getLogger(__name__)


# Create your views here.

class RegisterUserAPIView(APIView):
    http_method_names = ['post']

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        print(self.request.user)
        return UserProfile.objects.all()


class ProjectListAPIView(APIView):
    http_method_names = ['get', 'post']
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        projects = Project.objects.all()
        serializer = ProjectSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ProjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data)
        return Response(serializer.errors)


# class ProjectDetailAPIView(APIView):
#     http_method_names = ['get', 'put', 'delete']
#
#     def get(self, request, pk):
#         project = get_object_or_404(Project, pk=pk)
#         serializer = ProjectSerializer(data=project)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)
#
#     {
#         "non_field_errors": [
#             "Invalid data. Expected a dictionary, but got Project."
#         ]
#     }
#
#     def put(self, request, pk):
#         project = get_object_or_404(Project, pk=pk)
#         serializer = ProjectSerializer(instance=project, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk):
#         project = get_object_or_404(Project, pk=pk)
#         project.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)

class ProjectDetailAPIView(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           generics.GenericAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        print('in here')
        creator = self.request.user
        executor = get_object_or_404(User, pk=self.request.data['executor_id'])
        logger.info("{self.request.user} created a new task with id: {request.data.get('task_id'}")
        logger.info("{self.request.user} set as executor id: {request.data.get('executor_id')}")
        if serializer.is_valid():
            serializer.save(creator=creator, executor=executor)
            print(serializer.data)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MemberProjectViewSet(viewsets.ModelViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer

    def perform_create(self, serializer):
        member = get_object_or_404(User, pk=self.request.data['member_id'])
        project = get_object_or_404(Project, pk=self.request.data['project_id'])
        logger.info("there is a new member with id: {request.data.get('member_id')}")
        if serializer.is_valid():
            serializer.save(member=member, project=project)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDocumentViewSet(viewsets.ModelViewSet):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer

    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskCommentViewSet(viewsets.ModelViewSet):
    queryset = TaskComment.objects.all()
    serializer_class = TaskCommentSerializer
    permission_classes = (IsAuthenticated, )


    def perform_create(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_update(self, serializer):
        creator = self.request.user
        task = get_object_or_404(Task, pk=self.request.data['task_id'])
        if serializer.is_valid():
            serializer.save(creator=creator, task=task)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

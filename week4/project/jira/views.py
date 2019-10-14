from django.http import Http404
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import UserProfile, Project, ProjectMember, Task, TaskComment, TaskDocument
from .serializers import UserSerializer, ProjectSerializer, ProjectMemberSerializer, TaskDocument, TaskSerializer, \
    TaskCommentSerializer, TaskDocumentSerializer


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
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ProjectDetailAPIVeiw(mixins.RetrieveModelMixin,
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


class ProjectMemberViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = ProjectMember.objects.all()
    serializer_class = ProjectMemberSerializer


#
# class BlockViewSet(mixins.RetrieveModelMixin,
#                    mixins.UpdateModelMixin,
#                    mixins.DestroyModelMixin,
#                    mixins.CreateModelMixin,
#                    viewsets.GenericViewSet):
#     queryset = Block.objects.all()
#     serializer_class = BlockSerializer


class Task_List(generics.ListCreateAPIView):
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Task.objects.filter(creator=self.request.user)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskListDetail(generics.RetrieveDestroyAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        try:
            project = Project.objects.get(id=self.kwargs['pk'])
        except:
            raise Http404

        return Task.objects.filter(project=project)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskCommentAPIView(generics.ListCreateAPIView):
    serializer_class = TaskCommentSerializer

    def get_queryset(self):
        try:
            task = Task.objects.get(id=self.kwargs['pk'])
        except:
            raise Http404

        return TaskComment.objects.filter(task=task)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)


class TaskDocumentViewSet(mixins.RetrieveModelMixin,
                           mixins.UpdateModelMixin,
                           mixins.DestroyModelMixin,
                           mixins.CreateModelMixin,
                           viewsets.GenericViewSet):
    queryset = TaskDocument.objects.all()
    serializer_class = TaskDocumentSerializer





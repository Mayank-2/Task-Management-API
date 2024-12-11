from .models import Task
from .serializers import TaskSerializer, UpdateTaskSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from account.authentication import CustomAuthentication
from rest_framework.permissions import IsAuthenticated


class Tasks(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            tasks = Task.objects.filter(assigned_to=user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        user = request.user
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            title = serializer.validated_data.get("title")
            description = serializer.validated_data.get("description")
            task_status = serializer.validated_data.get("status")
            priority = serializer.validated_data.get("priority")
            due_date = serializer.validated_data.get("due_date")
            task = Task(assigned_to=user, title=title, description=description,
                        status=task_status, priority=priority, due_date=due_date)

            task.save()

            return Response({"message": "created"}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        try:
            task_id = request.data['id']
            task = Task.objects.get(id=task_id)
            serializer = UpdateTaskSerializer(
                task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            task = Task.objects.get(id=id)
            task.delete()
            return Response({"message": "Task deleted"}, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class GetTask(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, id):
        try:
            task = Task.objects.get(id=id)
            serializer = TaskSerializer(task)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)


class FilterTask(APIView):
    authentication_classes = [CustomAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, filter, query):
        user = request.user
        try:
            tasks = Task.objects.filter(**{filter: query}, assigned_to=user)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SortTask(APIView):
    def get(self, request, filter):
        user = request.user
        try:
            tasks = Task.objects.filter(assigned_to=user).order_by(filter)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class SearchTask(APIView):
    def get(self, request, query):
        user = request.user
        try:
            tasks = Task.objects.filter(
                assigned_to=user, title__icontains=query)
            serializer = TaskSerializer(tasks, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({"error": "Not Found"}, status=status.HTTP_404_NOT_FOUND)

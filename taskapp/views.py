from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from taskapp.models import Task
from taskapp.permissions import IsAdmin, IsSuperAdmin, IsUser
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
User = get_user_model() 


'''User Registeration'''
class RegisterUserAPIView(APIView):
    def post(self,request):
        serializer_data = UserSerializer(data = request.data)
        if serializer_data.is_valid():
            user = serializer_data.save()
            user.set_password(serializer_data.validated_data['password'])
            user.save()
            return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"User registration failed","error":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)




'''Login using username and password'''
class LoginUser(APIView):
    def post(self,request):
        username  = request.data.get('username')
        password  = request.data.get('password')
        user_data = authenticate(username=username,password=password)
        if user_data is not None:
            login(request,user_data)
            refresh = RefreshToken.for_user(user_data)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)
 
            print(f"Tokens generated: access={access_token}, refresh={refresh_token}")  
            response = Response({
                "status": "success",
                "message": "Logged in successfully!",
                "access_token": access_token,
            }, status=status.HTTP_200_OK)
            response.set_cookie(key="refresh_token",value=refresh_token,httponly=True,secure=False,samesite='None')
            return response
        return Response({"error":"Invalid credentials"},status=status.HTTP_401_UNAUTHORIZED)
    

# Superadmin section
'''Superadmin creating and managing admin'''

class SuperViewAdmin(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self,request):
        admin_list = User.objects.filter(role='admin')
        serializer = UserSerializer(admin_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer_data = UserSerializer(data = request.data)
        if serializer_data.is_valid():
            user = serializer_data.save(role='admin')
            user.set_password(serializer_data.validated_data['password'])
            user.save()
            return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"User registration failed","error":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        user_id =  request.query_params.get('user_id')
        if not user_id:
            return Response({"message" :"Userid is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_check  = User.objects.get(id=user_id,role="admin")
            user_check.delete()
            return Response({"message":"Successfully deleted admin"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message":"Admin not found"},status=status.HTTP_404_NOT_FOUND)

    #  delete, assign roles, and promote/demote admin
    def patch(self,request):
        try:
            user_id = request.data.get('user_id')
            new_role = request.data.get('new_role')

            user_check  = User.objects.get(id=user_id)
            user_check.role = new_role
            user_check.save()
            return Response({"message":"User role updated"},status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_200_OK)

'''Superadmin creating and managing admin'''

class SuperViewUser(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self,request):
        admin_list = User.objects.filter(role='user')
        serializer = UserSerializer(admin_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer_data = UserSerializer(data = request.data)
        if serializer_data.is_valid():
            user = serializer_data.save(role='user')
            user.set_password(serializer_data.validated_data['password'])
            user.save()
            return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"User registration failed","error":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        user_id =  request.query_params.get('user_id')
        if not user_id:
            return Response({"message" :"Userid is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            user_check  = User.objects.get(id=user_id,role="user")
            user_check.delete()
            return Response({"message":"Successfully deleted user"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message":"User not found"},status=status.HTTP_404_NOT_FOUND)
   

    #  Updating user
    def patch(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)  # Update user
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


'''Superadmin Can manage tasks and view all task completion reports.'''

class SuperCreateTask(APIView):
    permission_classes = [IsSuperAdmin]

    def get(self,request):
        task_list = Task.objects.all()
        serializer = TaskSerializer(task_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer_data = TaskSerializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({"message":"User created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"User registration failed","error":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        task_id =  request.query_params.get('task_id')
        if not task_id:
            return Response({"message" :"Task_id is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            task_check  = Task.objects.get(id=task_id)
            task_check.delete()
            return Response({"message":"Successfully deleted task"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
   

    #  Updating user
    def patch(self, request):
        user_id = request.data.get('user_id')

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=request.data, partial=True)  # Update user
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    



# Admin section
'''Admin Can manage tasks and view all task completion reports.'''

class AdminCreateTask(APIView):
    permission_classes = [IsAdmin]

    def get(self,request):
        task_list = Task.objects.all()
        serializer = TaskSerializer(task_list,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    

    def post(self,request):
        serializer_data = TaskSerializer(data = request.data)
        if serializer_data.is_valid():
            serializer_data.save()
            return Response({"message":"Task created successfully"},status=status.HTTP_201_CREATED)
        else:
            return Response({"message":"Task registration failed","error":serializer_data.errors},status=status.HTTP_400_BAD_REQUEST)
   
    def delete(self,request):
        task_id =  request.query_params.get('task_id')
        if not task_id:
            return Response({"message" :"Task_id is required"},status=status.HTTP_400_BAD_REQUEST)
        try:
            task_check  = Task.objects.get(id=task_id)
            task_check.delete()
            return Response({"message":"Successfully deleted task"},status=status.HTTP_404_NOT_FOUND)
        except User.DoesNotExist:
            return Response({"message":"Task not found"},status=status.HTTP_404_NOT_FOUND)
   

    #  Updating task
    def patch(self, request):
        user_id = request.data.get('user_id')
        new_status  = request.data.get('new_status')
        data ={
            "status":new_status
        }
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(user, data=data, partial=True)  # Update user
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"message": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


'''Admin Can view task completion reports for tasks assigned to users. '''

class AdminViewReport(APIView):
    permission_classes = [IsAdmin]

    def post(self,request):
        admin = request.user
        task_data = Task.objects.filter(created_by=admin,status="Completed")
        serializer = TaskSerializer(task_data,many=True)
        return Response({"message": "Task Completion Reports", "data": serializer.data}, status=status.HTTP_200_OK)



'''User Can view their assigned tasks, update their task status, and submit a
completion report (including worked hours).'''
class UserCreation(APIView):
    permission_classes = [IsUser]

    def patch(self, request):
        """Users can update task status and submit completion report"""
        task_id = request.data.get("task_id")
        status = request.data.get("status")
        completion_report = request.data.get("completion_report")
        worked_hours = request.data.get("worked_hours")
        try:
            task = Task.objects.get(id=task_id, assigned_to=request.user)
        except Task.DoesNotExist:
            return Response({"message": "Task not found or not assigned to you"}, status=status.HTTP_404_NOT_FOUND)

        if status:
            task.status = status
        if completion_report:
            task.completion_report = completion_report
        if worked_hours:
            task.worked_hours = worked_hours

        task.save()
        return Response({"message": "Task updated successfully"}, status=status.HTTP_200_OK)
    
    def get(self,request):
        user = request.user
        assigned_task = Task.objects.filter(assigned_to=user)
        assigned_user = TaskSerializer(assigned_task,many=True)
        return Response({assigned_task.data},status=status.HTTP_200_OK)
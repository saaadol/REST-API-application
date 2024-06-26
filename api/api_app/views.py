from rest_framework.response import Response
from rest_framework.decorators import api_view 
from .models import Data
from .serializers import DataSerializer, TodoSerializer
from rest_framework.exceptions import NotFound
from rest_framework.renderers import JSONRenderer

@api_view(["GET"])
def getTodos(request, pk):
    try:
        data = Data.objects.get(pk=pk)
    except Data.DoesNotExist:
        raise NotFound("key not found")
    todos_list = []
    for todo in data.todos.all():
        todo_values = {
            'todoName': todo.todoName,
            'description': todo.description,
            'isCompleted': todo.isCompleted,
        }
        todos_list.append(todo_values)
    return Response(todos_list)

@api_view(["GET"])
def getData(request):
    data = Data.objects.all()

    serializer = DataSerializer(data, many = True)
    return Response(serializer.data)

@api_view(["POST"])   
def PostData(request): 
    serializer = DataSerializer(data = request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

#Todo
@api_view(["POST"])   
def PostTodo(request): 
    userId =  request.data.get('userid')

    try:
      user_data = Data.objects.get(username=userId)
    except Data.DoesNotExist:
        return Response({"error": "User does not exist."}, status=400)
    
    # Update the request data with the actual user ID reference
    request.data['userid'] = user_data.pk

    serializer = TodoSerializer(data=request.data)    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201) 
    return Response(serializer.errors, status=400)  
    # serializer = TodoSerializer(data = request.data)
    # if serializer.is_valid():
    #     serializer.save()
    #     return Response(serializer.data, status=201)
    # return Response(serializer.errors, status=400)

@api_view(["GET","PUT"])   
def PostDataId(request, pk):
    try:
        olddata = Data.objects.get(id = pk) 
    except:
        return Response("id not available", status=400)
    serializer = DataSerializer(olddata, data = request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)


@api_view(["GET","DELETE"])
def DeleteAll(request):
    allusers = Data.objects.all()
    allusers.delete()
    return Response("Ressources Deleted", 201)


@api_view(["GET", "DELETE"])
def DeleteDataId(request, pk):
    try:
        userdata = Data.objects.get(id = pk)
        userdata.delete()
        return Response("Deleted", status=200)
    except:
        return Response("id not available", status=400)


# Create your views here.

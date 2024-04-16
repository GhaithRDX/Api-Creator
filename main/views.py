from django.shortcuts import render
from rest_framework.decorators import api_view ,authentication_classes,permission_classes
from rest_framework import status
from rest_framework.response import Response 
from .models import Modelnames , Projects,CustomUser
from .serializers import dynamic_serializer ,UserRegistrationSerializer,UserSerializer,models_S,DynamicModelFieldSerializer,projects_S
from dynamic_models.models import ModelSchema, FieldSchema
from django.db import models ,connection
from django.urls import clear_url_caches
from importlib import import_module,reload
from django.contrib import admin
from django.conf import settings
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.db import connection
from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from .permissions import Read , Write , No ,User1 , User2
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAdminUser

ftypes =['character','text','integer','float','boolean','date','foreignkey','ForeignKey','Foreignkey','foreignKey']

@api_view(['GET','POST'])
@permission_classes([])
def test(request):  
    print(request.user.username)
    print(request.user.co_owner.id)
    if request.user.co_owner == None :
        print("None 1")
    else:
        print(request.user.co_owner)
    return Response(status=status.HTTP_200_OK)


@permission_classes([IsAdminUser])
class SignupAPIView(APIView):
    def post(self, request):
        data = request.data.copy()
        data['co_owner']=''
        data['read_P']='True'
        data['write_P']='True'
        data['user1']='True'
        data['user2']='False'
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@permission_classes([IsAdminUser | User1])
class SignupAPIView2(APIView):
    def post(self, request):
        data = request.data.copy()
        data['co_owner']=request.user.id
        data['user1']='False'
        data['user2']='True'
        serializer = UserRegistrationSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def user_list(request,pk):
    user = CustomUser.objects.get(id=pk)
    serializer = UserSerializer(user)
    return Response(serializer.data)



# @api_view(['POST'])
# def Create2(request):
#     modelExists = False
#     modelCreated = False
#     modelName = request.POST.get('modelname', '')

#     if not modelName:
#         return Response({'Error': 'Model name is required.'}, status=status.HTTP_400_BAD_REQUEST)

#     user = request.user
#     modeld = ModelSchema.objects.all()

#     try:
#         model_schema = ModelSchema.objects.create(name=modelName)
#         modelCreated = True
#     except Exception as e:
#         modelExists = True
#         return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
#     fields = {}

#     len_req = (len(request.POST) - 1) // 5
#     count = 0

#     for x in range(len_req):
#         count += 1
#         field_name = request.POST.get('field' + str(count), '')
#         data_type = request.POST.get('datatype' + str(count), '')

#         if not field_name or not data_type:
#             return Response({'Error': 'Field name and data type are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         # For ForeignKey fields, you can handle them differently
#         if data_type == 'ForeignKey':
#             related_model_name = request.POST.get('related_model' + str(count), '')

#             if not related_model_name:
#                 return Response({'Error': 'Related model is required for ForeignKey field.'}, status=status.HTTP_400_BAD_REQUEST)

#             # Get the related model dynamically, assuming you have a ModelSchema for related models
#             try:
#                 related_model_schema = ModelSchema.objects.get(name=related_model_name)
#                 related_model = related_model_schema.as_model()
#             except ModelSchema.DoesNotExist:
#                 return Response({'Error': f'Related model "{related_model_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

#             try:
#                 is_unique = request.POST.get('unique' + str(count), False) == 'true'
#                 is_null = request.POST.get('null' + str(count), False) == 'true'
#             except Exception as e:
#                 return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)

#             fields[field_name] = models.ForeignKey(related_model, on_delete=models.CASCADE,unique=is_unique,null=is_null)
#         else:
#             # Handle other data types
#             is_unique = request.POST.get('unique' + str(count), False) == 'true'
#             is_null = request.POST.get('null' + str(count), False) == 'true'
#             max_length = int(request.POST.get('maxlen' + str(count), 255))
            
#             if data_type == 'character':
#                 max_length = int(request.POST.get('maxlen' + str(count), 255))
#                 fields[field_name] = models.CharField(max_length=max_length,unique=is_unique,null=is_null)
#             elif data_type == 'text':
#                 fields[field_name] = models.TextField(max_length=max_length,unique=is_unique,null=is_null)
#             elif data_type == 'integer':
#                 fields[field_name] = models.IntegerField(unique=is_unique,null=is_null)
#             elif data_type == 'float':
#                 fields[field_name] = models.FloatField(unique=is_unique,null=is_null)
#             elif data_type == 'boolean':
#                 fields[field_name] = models.BooleanField(null=is_null)
#             elif data_type == 'date':
#                 fields[field_name] = models.DateField(null=is_null)


#     fields['__module__'] = 'main.models'
    
#     # Dynamically create the model class
#     dynamic_model = type(modelName, (models.Model,), fields)
#     # Register the dynamic model with the admin
#     model_create = Modelnames.objects.create(user = user,modelname=request.POST['modelname']) 
#     admin.site.register(dynamic_model)
#     reload(import_module(settings.ROOT_URLCONF))
#     clear_url_caches()
#     return Response(status=status.HTTP_200_OK)
#

@permission_classes([IsAdminUser | User1])
@api_view(['POST'])
def Create(request):
        
    # len_req = (len(request.POST) -1) // 5
    len_req= request.POST['nf']
    project = request.POST['project']
    count = 0
        
    key =False
    modelName = request.POST['modelname']+"_"+str(request.user.id)
    
    print(modelName)
    
    fkey_name=''
    related_model_schema=''
    related_model_name=''        
    user = request.user
    modeld = ModelSchema.objects.all()
    
    if int(len_req) != int(((len(request.POST)-3)//5)):
        return Response({'Parameters Error':'Less parameters than expected ! .'}, status=status.HTTP_400_BAD_REQUEST)
    
    
    try : 
        project_model=Projects.objects.get(user=request.user.id,name = project)
    except Exception as e:
        return Response({'Project Error ':str(e)},status=status.HTTP_404_NOT_FOUND)
    
    try:
        model_create = Modelnames.objects.create(user = user,modelname=modelName,project = project_model)
    except Exception as e:
        return Response({'Error':'invalid model name .'},status = status.HTTP_400_BAD_REQUEST)
    
    try:
        model_schema = ModelSchema.objects.create(name=modelName)
    except Exception as e:
        return Response({'Creation Error':str(e)},status= status.HTTP_400_BAD_REQUEST)
        
    try:
        # len_req = (len(request.POST) -1) // 5
        len_req= int(request.POST['nf'])
        count = 0
        for x in range(len_req):
            count = count + 1
            field_name = request.POST.get('field' + str(count), '')
            data_type = request.POST.get('datatype' + str(count), '')
            is_unique = request.POST.get('unique' + str(count), False) == 'true'
            is_null = request.POST.get('null' + str(count), False) == 'true'
            max_length = int(request.POST.get('maxlen' + str(count), 255))
            
            if not field_name or not data_type:
                return Response({'Error': 'Field name and data type are required.'}, status=status.HTTP_400_BAD_REQUEST)

            if request.POST['datatype'+ str(count)] not in ftypes:
                return Response({'Error':'Invalid data type !'} , status=status.HTTP_400_BAD_REQUEST)
            
            if data_type == 'foreignkey':
                key=True
                fkey_name=field_name
                related_model_name = request.POST.get('related_model' + str(count), '')
                
                try:
                    related_model_schema = ModelSchema.objects.get(name=related_model_name)
                    related_model = related_model_schema.as_model()
                except ModelSchema.DoesNotExist:
                    return Response({'Error': f'Related model "{related_model_name}" does not exist.'}, status=status.HTTP_400_BAD_REQUEST)

            else:     
                field_schema = FieldSchema.objects.create(
                    name=request.POST['field' + str(count)],
                    data_type=request.POST['datatype' + str(count)],
                    model_schema=model_schema,
                    max_length=request.POST['maxlen' + str(count)],
                    null=request.POST['null' + str(count)],
                    unique=request.POST['unique' + str(count)]
                    )
                
        reg_model = model_schema.as_model()
        
    
        if key:
            class NewForeignKeyField(models.ForeignKey):
                    def __init__(self, *args, **kwargs):
                        kwargs['to'] = related_model_name  
                        kwargs['on_delete'] = models.CASCADE  
                        kwargs['related_name'] = 'test'  
                        super().__init__(*args, **kwargs)
                        
            reg_model.add_to_class(fkey_name, NewForeignKeyField())
            with connection.schema_editor() as schema_editor:
                schema_editor.add_field(reg_model, reg_model._meta.get_field(fkey_name))
        
        admin.site.register(reg_model)
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()
        
        return Response(status= status.HTTP_200_OK)
    except Exception as e2:
                return Response({'Error':str(e2)},status = status.HTTP_400_BAD_REQUEST)



# @api_view(['POST'])
# def CreateProject(request):
#     user = request.user
#     name = request.POST['name']
#     try : 
#         Projects.objects.create(user = user,name=name)
#         return Response(status=status.HTTP_201_CREATED)
#     except Exception as e:
#         return Response({'Error ':str(e)},status = status.HTTP_400_BAD_REQUEST)
# E

@api_view(['GET','POST'])
@permission_classes([IsAdminUser | User1])
def UserProjects(request):
    if request.method == 'GET':
        try:
            projects =Projects.objects.filter(user=request.user.id)
            try:
                serializer = projects_S(projects, many=True)
                return Response(serializer.data ,status= status.HTTP_200_OK)
            
            except Exception as e1:
                return Response({'Error ':str(e1)}, status = status.HTTP_400_BAD_REQUEST)
                
        except Exception as e:
            return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'POST':
        user = request.user
        name = request.POST['name']
        try : 
            Projects.objects.create(user = user,name=name)
            return Response(status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'Error ':str(e)},status = status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def project_models(request,id):

    try:
        owner = Projects.objects.get(id=id).user
        if request.user != owner:
            return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
        project = Projects.objects.get(id = id)
        models=Modelnames.objects.filter(user=request.user.id,project=project)
        
        for model in models:
            model.modelname = model.modelname.rsplit('_', 1)[0]

        serializer = models_S(models, many=True)
        return Response(serializer.data ,status= status.HTTP_200_OK)
    except Exception as e:
        return Response({'Error ':str(e)}, status = status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE','PUT'])
@permission_classes([IsAdminUser | User1])
def edit_project(request,id):
    
    try:
        project = Projects.objects.get(id = id)
    except Projects.DoesNotExist :
        return Response(status= status.HTTP_404_NOT_FOUND)
    
    if request.method == 'DELETE':   
        try :
            models =Modelnames.objects.filter(user=request.user.id,project=project).values()
            for m in models :
                model1 = ModelSchema.objects.get(name= m['modelname'])
                mod1 = Modelnames.objects.get(modelname=m['modelname'])
                model = model1.as_model()
                admin.site.unregister(model)
                mod1.delete()
                model1.delete()
                
            project.delete()
            reload(import_module(settings.ROOT_URLCONF))
            clear_url_caches()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    elif request.method == 'PUT':
        try:
            serializer = projects_S(project , data= request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)

        
@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def user_model(request):
    try:
        models=Modelnames.objects.filter(user=request.user.id)
        try:
            for model in models:
                model.modelname = model.modelname.rsplit('_', 1)[0]

            serializer = models_S(models, many=True)
            return Response(serializer.data ,status= status.HTTP_200_OK)
        
        except Exception as e1:
            print("error:   " , e1)
            
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
        
        
    return Response(status = status.HTTP_200_OK)


@api_view(['DELETE'])
@permission_classes([IsAdminUser | User1])
def dele(request,name):
    try :
        modelName = name+"_"+str(request.user.id)

        model1 = ModelSchema.objects.get(name= modelName)
        mod1 = Modelnames.objects.get(modelname=modelName)
        model = model1.as_model()
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_404_NOT_FOUND)
    
    try:
        if request.user != mod1.user:
            return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
        admin.site.unregister(model)
        mod1.delete()
        model1.delete()
        reload(import_module(settings.ROOT_URLCONF))
        clear_url_caches()
        return Response(status = status.HTTP_204_NO_CONTENT)
    except Exception as e4:
        return Response({'Error':str(e4)},status = status.HTTP_400_BAD_REQUEST)
    
    

@api_view(['POST'])
@permission_classes([IsAdminUser | User1 | (User2 and Write)])
def Model_data_in(request,name):
    
    try:
        modelName = name+"_"+str(request.user.id)

        mod1 = Modelnames.objects.get(modelname=modelName)
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_404_NOT_FOUND)
    
    if ( (mod1.user != request.user) and (mod1.user != request.user.co_owner) ):
        return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
    
    
    try:
        model1 = ModelSchema.objects.get(name= modelName)
        model = model1.as_model()
        dynamic_serializer1 =dynamic_serializer(model)
        serializer = dynamic_serializer1(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data , status = status.HTTP_201_CREATED)
            
        return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("ERROR ! : ",e)
        return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
    
    
    
@api_view(['GET'])
@permission_classes([IsAdminUser | User1 | (User2 and Read)])
def Model_data(request,name):
    
    modelName = name+"_"+str(request.user.id)

    mod1 = Modelnames.objects.get(modelname=modelName)
    if ((mod1.user != request.user) and (mod1.user != request.user.co_owner)): 
        return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
    
    
    try :
        #print(request.query_params)
        model1 = ModelSchema.objects.get(name= modelName)
        model = model1.as_model()
        try:
            dynamic_serializer1 =dynamic_serializer(model)
            mods = model.objects.all()
            serializer = dynamic_serializer1(mods, many=True)
            return Response(serializer.data ,status= status.HTTP_200_OK)
            
        except Exception as e:
            return Response({'Error ':str(e)} , status=status.HTTP_400_BAD_REQUEST)
        
    except Exception as e:
        return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)
    
    
@api_view(['DELETE','PUT'])
@permission_classes([IsAdminUser | User1 | (User2 and Write)])
def edit_pk(request,modelname,id):
        
    modelName = modelname+"_"+str(request.user.id)
    if request.method == 'DELETE':
        try :

            owner = Modelnames.objects.get(modelname=modelName).user
            if ((request.user != owner) and (owner != request.user.co_owner)):
                return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
            model1 = ModelSchema.objects.get(name= modelName)
            model = model1.as_model()
            ele = model.objects.get(id=id)
            ele.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({'Error ':str(e)},status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'PUT':
        try :
            owner = Modelnames.objects.get(modelname=modelName).user
            if ((request.user != owner) and (owner != request.user.co_owner)):
                return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
            model1 = ModelSchema.objects.get(name= modelName)
            model = model1.as_model()
            ele = model.objects.get(id=id)
            dynamic_serializer1 =dynamic_serializer(model)
            serializer = dynamic_serializer1(ele ,data =request.data)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
            
            return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
        except Exception as e:
            return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
    

# @api_view(['GET'])
# def model_name(request,name):
    
#     try :
#         #print(request.query_params)
#         model1 = ModelSchema.objects.get(name= name)
#         model = model1.as_model()
#         try:
#             dynamic_serializer1 =dynamic_serializer(model)
#             mods = model.objects.all()
#             serializer = dynamic_serializer1(mods, many=True)
#             return Response(serializer.data ,status= status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({'Error ':str(e)} , status=status.HTTP_400_BAD_REQUEST)
        
#     except Exception as e:
#         return Response({'Error':str(e)},status = status.HTTP_400_BAD_REQUEST)


# @api_view(['PUT'])
# def upd(request,modelname,id):
#     try :
#         owner = Modelnames.objects.get(modelname=modelname).user
#         if request.user != owner:
#             return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
#         model1 = ModelSchema.objects.get(name= modelname)
#         model = model1.as_model()
#         ele = model.objects.get(id=id)
#         dynamic_serializer1 =dynamic_serializer(model)
#         serializer = dynamic_serializer1(ele ,data =request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST)
        
#         return Response(serializer.data , status=status.HTTP_202_ACCEPTED)
#     except Exception as e:
#         return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)

  
        
@api_view(['GET'])
@permission_classes([IsAdminUser | User1])
def dynamic_model_fields(request, model_name):
    
    modelName = model_name+"_"+str(request.user.id)
    try:
        owner = Modelnames.objects.get(modelname=modelName).user
        if request.user != owner:
            return Response({'Error' : 'UNAUTHORIZED !'},status = status.HTTP_401_UNAUTHORIZED)
        
        model_schema = ModelSchema.objects.get(name=modelName)

        dynamic_model_class = model_schema.as_model()
        
        field_data = []
        
        for field in dynamic_model_class._meta.get_fields():    
            field_data.append({
                'name': field.name,
                'data_type': field.get_internal_type(),
                'max_length': field.max_length if hasattr(field, 'max_length') else None,
                'null': field.null,
                'unique': field.unique,
                'related_model':field.to if hasattr(field,'to') else None,
            })

        serializer = DynamicModelFieldSerializer(field_data, many=True)
        return Response(serializer.data,status = status.HTTP_200_OK)
    except Exception as e: 
        return Response({'Error':str(e)},status=status.HTTP_400_BAD_REQUEST)
        
    # except ContentType.DoesNotExist:
    #     return Response({'error': 'Dynamic model not found'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.http import HttpResponse
from .serializer import UsuarioSerializer, ContactoSerializer, EventoSerializer, ActividadesSerializer, ParticipantesSerializer, ContactoSerializerDetallado
from .models import Usuario, Contactos, Evento, Actividades, ParticipantesEventoActividad, User
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.settings import api_settings
from django.dispatch import receiver
from django.conf import settings
from django.db.models.signals import post_save

# --------------------------------------------------------------------------------
# Creando el CRUD
# Todas las vistas acá seran para crear y ver los modelos
# --------------------------------------------------------------------------------

# Método para crear un usuario.
# Primero crea un usuario de la relación "User" y luego se le asocian los argumentos
# que falten a la relación "Usuario"

@api_view(['GET','POST']) # Es un decorador que me sirve para renderizar en pantalla la vista basada en función.
def crear_usuario(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'POST':
        # Creamos el usuario (User)
        user = User.objects.create(
            email = request.data["email"],
            first_name = request.data["nombres"],
            last_name = request.data["apellidos"],
            password = request.data["password"],
            username = request.data["apodo"],
            is_active = True,
        )
        # Creamos su Token
        token = Token.objects.create(
            user=user
        )
        # Asociamos dicho usuario (User) a la relación Usuario.
        # Se debe actualizar porque ya se crea automaticamente el Usuario asociado
        # a la relación "user".
        usuario = Usuario.objects.get(
            user = user
        )
        usuario.foto = request.data["foto"]
        serializer = UsuarioSerializer(usuario, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class ContactoViews(viewsets.ModelViewSet):
    serializer_class = ContactoSerializerDetallado
    queryset = Contactos.objects.all()

class EventoViews(viewsets.ModelViewSet):
    serializer_class = EventoSerializer
    queryset = Evento.objects.all()

class ActividadesViews(viewsets.ModelViewSet):
    serializer_class = ActividadesSerializer
    queryset = Actividades.objects.all()
    
class ParticipantesViews(viewsets.ModelViewSet):
    serializer_class = ParticipantesSerializer
    queryset = ParticipantesEventoActividad.objects.all()

# --------------------------------------------------------------------------------
# Registro y Login
# --------------------------------------------------------------------------------

# Método para que un usuario se logee
@api_view(['POST'])
def login_user(request):
    print("user:",request.data) 
    try:
        user = User.objects.get(email=request.data["email"], password=request.data["password"])
    except User.DoesNotExist:
        return Response({"error": True, "error_cause": 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
    token = Token.objects.get(user=user)
    reqdata = {
        "token": token.key,
        "nickname": user.username
    }
    return Response({"answer": True, "description": reqdata }, status=status.HTTP_200_OK)

# --------------------------------------------------------------------------------
# Gestión de contactos
# --------------------------------------------------------------------------------

# Para agregar un contacto

@api_view(['POST']) # Es un decorador que me sirve para renderizar en pantalla la vista basada en función.
def agregar_contacto(request):
    correo_usuario = request.data["correo_usuario"]
    correo_contacto = request.data["correo_contacto"]
    # Determinamos si el usuario existe
    try:
        user = User.objects.get(email=correo_usuario)
    except User.DoesNotExist:
        return Response({"error":True, "error_causa":"El usuario no existe!"}, status=status.HTTP_404_NOT_FOUND)
    
    # Determinamos si el contacto existe.
    try:
        contact = User.objects.get(email=correo_contacto)
    except User.DoesNotExist:
        return Response({"error":True, "error_causa":"El usuario-contacto no existe!"}, status=status.HTTP_404_NOT_FOUND)

    # Determinamos si el usuario tiene agregado el contacto.
    # Si no existe lo crea y lo agrega.
    try:
        contacto = Contactos.objects.get(usuario=user, contacto=contact)
        return Response({"error":True, "mensaje":"El usuario ya tiene agregado el contacto!"}, status=status.HTTP_400_BAD_REQUEST)
    except Contactos.DoesNotExist:
        contacto_nuevo =    {
            'usuario': user.id,
            'contacto': contact.id
        }
        serializer = ContactoSerializer(data=contacto_nuevo)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            contacto = Contactos(**validated_data)
            contacto.save()
            serializer_response = ContactoSerializer(contacto)
            return Response(serializer_response.data, status=status.HTTP_201_CREATED)
        else:
            return Response({"error":True, "mensaje":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Para eliminar un contacto

@api_view(['POST'])
def eliminar_contacto(request):
    correo_usuario = request.data["correo_usuario"]
    correo_contacto = request.data["correo_contacto"]
    # Determinamos si el usuario existe
    try:
        user = User.objects.get(email=correo_usuario)
    except User.DoesNotExist:
        return Response({"error":True, "error_causa":"El usuario no existe!"}, status=status.HTTP_404_NOT_FOUND)
    
    # Determinamos si el contacto existe.
    try:
        contact = User.objects.get(email=correo_contacto)
    except User.DoesNotExist:
        return Response({"error":True, "error_causa":"El usuario-contacto no existe!"}, status=status.HTTP_404_NOT_FOUND)

    # Determinamos si el usuario tiene agregado el contacto.
    # Si no lo tiene agregado arroja un error.
    try:
        contacto = Contactos.objects.get(usuario=user, contacto=contact)
    except Contactos.DoesNotExist:
        return Response({"error":True, "mensaje":"El usuario-contacto no está agregado en la lista de contactos del usuario!"}, status=status.HTTP_404_NOT_FOUND)

    # Determinamos si el usuario tiene un evento asociado
    """
    Un usuario está asociado a un evento si:
    - El usuario no ha creado algún evento.
    - El usuario no ha sido agregado a alguna actividad de un evento.
    """
    # consultamos la tabla "Evento", para ver si el contacto creó un evento.
    try:
        evento = Evento.objects.get(id_usuario=contact)
        return Response({"error":True, "mensaje":"El contacto tiene un evento creado; evento: '{nombre_evento}'".format(nombre_evento=evento.nombre)}, status=status.HTTP_400_BAD_REQUEST)
    except Evento.DoesNotExist:
        print("El contacto no tiene un evento creado!")

    # consultamos la tabla "ParticipantesEventoActividad", para ver si el contacto
    # ha sido agregado a un evento.
    try:
        participantes_eventos = ParticipantesEventoActividad.objects.get(id_participante=contacto)
        return Response({"error":True, "mensaje":"El contacto está asociado a una actividad de un evento; actividad: '{nombre_actividad}', evento: '{nombre_evento}'".format(nombre_actividad=participantes_eventos.id_actividad.descripcion, nombre_evento=participantes_eventos.id_evento.nombre)}, status=status.HTTP_400_BAD_REQUEST)
    except ParticipantesEventoActividad.DoesNotExist:
        print("El contacto no está agregado a alguna actividad de un evento!")
    
    # Finalmente, si pasa todas las pruebas, se elimina el contacto.
    contacto.delete()
    return Response({"error":True, "mensaje":"El usuario-contacto fue eliminado éxitosamente!"}, status=status.HTTP_200_OK)

#experimental
@api_view(['POST'])
def UsuarioSingUpViews(request):
    serializer = UsuarioSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        #user = User.objects.get(username=request.data['correo_electronico'])#username en comillas
        #user.set_password(request.data['password'])
        #user.save()
        #token = Token.objects.create(user=user)
        user = Usuario.objects.create(
            correo_electronico=request.data['correo_electronico'],
            password=request.data['password'],
            nombres=request.data['nombres'],
            apellidos=request.data['apellidos'],
            apodo=request.data['apodo'],
            foto=request.data['foto']
            
        )
        token = Token.objects.get_or_create(user=user)
        return Response({"token": token.key, "user": serializer.data})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def UsuarioLoginViews(request):
    return Response({})

@api_view(['GET'])
def TestToken(request):
    return Response({})
##
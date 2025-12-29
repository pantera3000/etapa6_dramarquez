from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

class CaseInsensitiveModelBackend(ModelBackend):
    """
    Backend de autenticación que permite login con nombre de usuario
    insensible a mayúsculas y minúsculas.
    
    Ejemplo: 'Usuario' == 'usuario' == 'USUARIO'
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            # Búsqueda insensible a mayúsculas (__iexact)
            case_insensitive_username_field = '{}__iexact'.format(UserModel.USERNAME_FIELD)
            user = UserModel.objects.get(**{case_insensitive_username_field: username})
        except UserModel.DoesNotExist:
            # Ejecutar hasher por defecto para evitar ataques de timing
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

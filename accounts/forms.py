from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico", required=True)
    first_name = forms.CharField(label="Nombre", max_length=30, required=True)
    last_name = forms.CharField(label="Apellidos", max_length=150, required=True)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')  # Include password1 and password2

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configure username field
        self.fields['username'].label = "Usuario"
        self.fields['username'].widget.attrs.update({'placeholder': 'Ej: alopez18'})

        self.fields['first_name'].widget.attrs.update({'placeholder': 'Ej: Alejandro'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Ej: González Pérez'})
        self.fields['email'].widget.attrs.update({'placeholder': 'ej: a.gonzalez@example.com'})

        if 'password1' in self.fields:
            self.fields['password1'].label = "Contraseña"
            self.fields['password1'].widget.attrs.update({'placeholder': 'Ingrese su contraseña'})
            self.fields['password1'].help_text = _("<ul>"
                                                "<li>No puede ser muy similar a tu otra información personal.</li>"
                                                "<li>Debe tener al menos 8 caracteres.</li>"
                                                "<li>No puede ser una contraseña demasiado común.</li>"
                                                "<li>No puede ser enteramente numérica.</li>"
                                            "</ul>")
        
        if 'password2' in self.fields:
            self.fields['password2'].label = "Confirmar contraseña"
            self.fields['password2'].help_text = _("Ingrese la misma contraseña que antes, para verificación.")
            self.fields['password2'].widget.attrs.update({'placeholder': 'Repita su contraseña'})
        
        # Ensure a consistent field order
        field_order = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        
        # Create a new OrderedDict for fields based on field_order
        ordered_fields = {}
        for field_name in field_order:
            if field_name in self.fields:
                ordered_fields[field_name] = self.fields[field_name]
        
        # Add any other fields that might not be in field_order (e.g., from future Django versions or plugins)
        for field_name, field_obj in self.fields.items():
            if field_name not in ordered_fields:
                ordered_fields[field_name] = field_obj
        
        self.fields = ordered_fields

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Spanish labels and placeholders
        self.fields['username'].label = "Usuario"
        self.fields['username'].widget.attrs.update({'placeholder': 'Usuario'})
        self.fields['password'].label = "Contraseña"
        self.fields['password'].widget.attrs.update({'placeholder': 'Contraseña'})

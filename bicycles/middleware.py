class UTF8ResponseMiddleware:
    """
    Middleware para asegurar que todas las respuestas HTTP tengan charset=utf-8 en el header Content-Type
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Si existe un Content-Type header pero no incluye charset
        if response.get('Content-Type') and 'charset' not in response.get('Content-Type'):
            if 'text/html' in response.get('Content-Type'):
                response['Content-Type'] = 'text/html; charset=utf-8'
            elif 'application/json' in response.get('Content-Type'):
                response['Content-Type'] = 'application/json; charset=utf-8'
            elif 'text/' in response.get('Content-Type'):
                # Para otros tipos de texto como text/css, text/javascript, etc.
                content_type = response.get('Content-Type').split(';')[0]
                response['Content-Type'] = f'{content_type}; charset=utf-8'
        
        # Para plantillas HTML renderizadas que podrían no tener Content-Type explícito
        if not response.get('Content-Type') and hasattr(response, 'charset'):
            response.charset = 'utf-8'
                
        return response

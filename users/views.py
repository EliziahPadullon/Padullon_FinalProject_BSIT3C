from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

from django.views import View
from users.models import Users
from users.forms import RegisterForm, LoginForm
from users.utils.hash_password import hash_password
from users.utils.generate_jwt import generate_jwt, decode_jwt


@csrf_exempt
@require_POST
def register(request):
    try:
        data = json.loads(request.body)
        form = RegisterForm(data)

        if form.is_valid():
            user = Users.objects.create(
                username=form.cleaned_data['username'],
                password=hash_password(form.cleaned_data['password']),
                email=form.cleaned_data['email'],
                name=form.cleaned_data['name']
            )
            token = generate_jwt(user)
            return JsonResponse({"token": token}, status=200)
        return JsonResponse({"error": form.errors}, status=400)

    except Exception as e:
        print("Register error:", str(e))
        return JsonResponse({"error": str(e)}, status=500)


@csrf_exempt
@require_POST
def login(request):
    try:
        data = json.loads(request.body)
        form = LoginForm(data)

        if form.is_valid():
            user = form.cleaned_data["user"]
            token = generate_jwt(user)
            return JsonResponse({"token": token}, status=200)
        return JsonResponse({"error": form.errors}, status=400)

    except Exception as e:
        print("Login error:", str(e))
        return JsonResponse({"error": str(e)}, status=500)

class ProtectedView(View):
    def dispatch(self, request, *args, **kwargs):
        # Step 1: Get Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return JsonResponse({'error': 'Unauthorized: No token provided'}, status=401)

        token = auth_header.split(' ')[1]

        # Step 2: Decode the token
        try:
            payload = decode_jwt(token)
            user_id = payload.get('user_id')

            # Step 3: Get the user
            try:
                user = Users.objects.get(id=user_id)
                request.user = user
            except Users.DoesNotExist:
                return JsonResponse({'error': 'User not found'}, status=404)

        except Exception as e:
            return JsonResponse({'error': f'Unauthorized: {str(e)}'}, status=401)

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return JsonResponse({'message': f'Hello, {request.user.username}! You accessed a protected route.'})
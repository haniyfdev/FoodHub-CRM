from channels.db import database_sync_to_async # db bilan async ishlash uchun
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model

User = get_user_model()

# -- -- -- -- -- -- -- -- -- --
@database_sync_to_async
def get_user(token_key):
    try:
        # token'ni tekshiramiz validation
        access_token = AccessToken(token_key)

        # token ichidan user_id'ni olamiz
        user_id = access_token['user_id']

        # bazadan foydalanuvchini topamiz
        return User.objects.get(id=user_id)
    except Exception:
        # Agar token xato bo'lsa, "Anonymous" qaytaramiz
        return AnonymousUser()
    
# -- -- -- -- -- -- -- -- -- --
class JwtAuthMiddleware:
    """WebSocket ulanayatganda URL orqali yuborilgan tokenni o'qiydi"""

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        # URL'dan token'ni qidiramiz
        query_string = scope.get("query_string", b"").decode("utf-8")
        token_key = None

        # 'token' qismini ajratib olamiz
        for param in query_string.split("&"):
            if param.startswith("token="):
                token_key = param.split("=")[1]

        # Agar token bo'lsa user-ni topamiz
        if token_key:
            scope['user'] = await get_user(token_key)
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)

        

from rest_framework.permissions import BasePermission, SAFE_METHODS

# -- -- -- -- -- -- -- -- --
class IsBossOrReadOnly(BasePermission):
    message = "Faqat admin edit qiladi"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        if not request.user or not request.user.is_authenticated:
            return False
        
        return(
            request.user.is_staff or 
            (hasattr(request.user, 'profile') and
             request.user.profile.role == 'boss')
        )
 
# -- -- -- -- -- -- -- -- --
class IsManagerOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        if not request.user or not request.user.is_authenticated:
            return False
        
        return (
            request.user.is_staff or hasattr(request.user, 'profile') and
            request.user.profile.role in ['boss', 'manager']
        )

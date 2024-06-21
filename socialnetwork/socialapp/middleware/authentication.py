from rest_framework import permissions
from rest_framework.views import APIView


class SomeProtectedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Your logic here
        pass

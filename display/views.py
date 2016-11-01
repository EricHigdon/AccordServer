from rest_framework import viewsets
from .serializers import SlideSerializer
from django.shortcuts import get_object_or_404
from bulletin.models import Church
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q

class SlideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows slides to be viewed.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Church.objects.all()
    serializer_class = SlideSerializer

    def get_queryset(self):
        church = get_object_or_404(Church, admins=self.request.user)
        now = timezone.now()
        return church.slides.filter(
            Q(start_date__lte=now, end_date__gte=now) |
            Q(start_date__lte=now, end_date__isnull=True)
        ).all()

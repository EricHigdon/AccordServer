from rest_framework import viewsets
from .serializers import SlideSerializer, CountdownSerializer
from django.shortcuts import get_object_or_404
from bulletin.models import Church
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.db.models import Q
from django.http import Http404

class SlideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows slides to be viewed.
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Church.objects.all()
    serializer_class = SlideSerializer

    def get_queryset(self):
        church = Church.objects.filter(admins=self.request.user)
        if len(church) == 0:
            raise Http404
        else:
            church = church.first()
        now = timezone.now()
        return church.slides.filter(
            Q(Q(start_date__isnull=True) | Q(start_date__lte=now))
            & Q(Q(end_date__isnull=True) | Q(end_date__gte=now))
        )
class CountdownViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for getting a church's countdowns
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = Church.objects.all()
    serializer_class = CountdownSerializer

    def get_queryset(self):
        church = Church.objects.filter(admins=self.request.user)
        if len(church) == 0:
            raise Http404
        return church[:1]

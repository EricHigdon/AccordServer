from .models import Slide
from rest_framework import viewsets
from .serializers import SlideSerializer


class SlideViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows slides to be viewed.
    """
    queryset = Slide.objects.all()
    serializer_class = SlideSerializer
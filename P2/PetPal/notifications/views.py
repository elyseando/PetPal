from django.shortcuts import get_object_or_404

from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.pagination import PageNumberPagination

from .serializers import NotificationSerializer
from .models import Notification


# Create your views here.
class SetPaginationNotification(PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    max_page_size = 10

class ListCreateNotification(ListCreateAPIView):
    serializer_class = NotificationSerializer
    pagination_class = SetPaginationNotification

    def get_queryset(self):
        queryset = Notification.objects.all()
        filter = self.request.query_params.get('filter')
        order = self.request.query_params.get('order')
        if filter is not None:
            if filter == 'read':
                is_read = True
            elif filter == 'unread':
                is_read = False
            queryset = queryset.filter(is_read=is_read)
        if order is not None:
            if order == 'latest':
                order_by = '-creation_time'
            elif order == 'oldest':
                order_by = 'creation_time'
            queryset = queryset.order_by(order_by)

        return queryset
    
    # t = type/app of notification
    # reverse(t:...)

class RetrieveDestroyNotification(RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer

    def get_object(self):
        notif = get_object_or_404(Notification, id=self.kwargs['pk'])
        if notif:
            notif.is_read = True

        return notif


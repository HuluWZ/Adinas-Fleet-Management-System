from django.core.serializers import serialize
from .models import Notification

def notifications(request):
    latest_notifications = Notification.objects.filter(is_seen=False).order_by('-created_at')
    notifications_json = serialize('json', latest_notifications)
    return {'latest_notifications': latest_notifications,'count':len(latest_notifications)}

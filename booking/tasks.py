from celery import shared_task
from datetime import timedelta , datetime
from .models import VehicleBooking , Notification
from accounts.models import UserAccount
from django.utils import timezone
from django.contrib import messages
from django.http import request
from django.db.models import Q
from utils.email_messages import sendUpcomingAndEndingEmail
import logging


logger = logging.getLogger(__name__)

@shared_task
def notify_upcoming_ending_bookings():
    two_days_from_now = timezone.now() + timedelta(days=2)
    two_days_before = timezone.now() - timedelta(days=2)

    upcoming_bookings = VehicleBooking.objects.filter(
        start_date__lte=two_days_from_now, start_date__gt=timezone.now()
    )

    ending_bookings = VehicleBooking.objects.filter(
        end_date__lte=two_days_from_now, end_date__gt=timezone.now()
    )

    logger.info(" Total Upcoming Bookings: %s", len(upcoming_bookings))
    logger.info(" Total Ending Bookings: %s", len(ending_bookings))
    for booking in upcoming_bookings:
        Notification.objects.create(
           title=f"New Vehicle Booking will start on {booking.start_date.strftime('%b %d, %Y')}.",
           message=f"{booking.no_of_vehicles} {booking.vehicle_type} booking from {booking.pickup} to {booking.drop_off} for {booking.duration} days will start on {booking.start_date.strftime('%b %d, %Y')}",
           type="Upcoming",
           booking=booking.id
        )
        send_admin_notification_email( booking, "Upcoming",booking.start_date)

    for booking in ending_bookings:
        Notification.objects.create(
         title=f"New Vehicle Booking will end on {booking.end_date.strftime('%b %d, %Y')}.",
         message=f"{booking.no_of_vehicles} {booking.vehicle_type} booking from {booking.pickup} to {booking.drop_off} for {booking.duration} days will end on {booking.end_date.strftime('%b %d, %Y')}",
         type="Ending",
         booking=booking.id
        )

        send_admin_notification_email( booking, "Ending",booking.end_date)

def send_notification_message(booking, event_type,date):
    logger.info("Booking #%s is %s in 2 days on %s ", booking.id, event_type,date.strftime("%B %d, %Y"))


def send_admin_notification_email(booking,event_type,date):
    staff_list = UserAccount.objects.filter(is_superuser=True)
    full_name = staff_list[0] if staff_list else "Staff Members"    
    staff_emails = [staff.email for staff in staff_list]
    data ={"event_type":event_type,"booking":booking,"date":date.strftime("%B %d, %Y"),"full_name":full_name}
    sendUpcomingAndEndingEmail(staff_emails,event_type,data) 


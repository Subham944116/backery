from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.permissions import AllowAny

from .serializers import ContactSerializer

class ContactView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        contact = serializer.save()

        # Email content
        subject = f"New Contact Message: {contact.subject}"
        message = f"""
New message received from Sweet Bakery website 🍰

Name: {contact.full_name}
Email: {contact.email}
Phone: {contact.phone}

Message:
{contact.message}
"""

        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,     # FROM bakery email
            [settings.ADMIN_EMAIL],          # TO admin
            fail_silently=False,
        )

        return Response(
            {   "id":  contact.id,
                "message": "Your message has been sent successfully ❤️"},
            status=status.HTTP_201_CREATED
        )

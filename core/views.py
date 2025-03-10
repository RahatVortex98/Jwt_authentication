from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from .models import Note
from .serializers import NoteSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# Create your views here.
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes= Note.objects.filter(owner=user)
    serializer = NoteSerializer(notes,many=True)

    return Response(serializer.data)
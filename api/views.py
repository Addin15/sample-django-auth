from django.shortcuts import render
from rest_framework import views, response

from . serializers import NoteSerializer
from . models import Note
from api import serializers

# Create your views here.


class NoteAPI(views.APIView):

    def post(self, request):

        serializers = NoteSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()

            return response.Response(data=serializers.data)
        else:
            return response.Response(data={"message": "Provided data is not valid"})

    def get(self, request):

        notes = Note.objects.all()
        serializers = NoteSerializer(notes, many=True)

        return response.Response(serializers.data)

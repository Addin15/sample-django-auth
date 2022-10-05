from rest_framework import serializers

from .models import Note


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('title', 'content')

    def create(self, validated_data):
        title = validated_data.get('title')
        content = validated_data.get('content')

        note = Note.objects.create(
            title=title,
            content=content,
        )

        return note

from rest_framework import serializers
from .models import AnalyzedString
from .utils import analyze_string


class AnalyzedStringSerializer(serializers.ModelSerializer):
    """
    Serializer for the AnalyzedString model.
    Handles automatic computation of string metrics before saving.
    """

    class Meta:
        model = AnalyzedString
        fields = '__all__'
        read_only_fields = [
            'length',
            'is_palindrome',
            'unique_characters',
            'word_count',
            'sha256_hash',
            'character_frequency_map',
        ]

    def create(self, validated_data):
        """
        Override create() to analyze the string before saving.
        """
        text = validated_data.get('text')

        # Use utility to compute analysis
        analyzed_data = analyze_string(text)

        # Merge computed fields with the validated input
        instance = AnalyzedString.objects.create(**validated_data, **analyzed_data)

        return instance

    def update(self, instance, validated_data):
        """
        Override update() to reanalyze string if 'text' changes.
        """
        text = validated_data.get('text', instance.text)

        # Only reanalyze if text actually changed
        if text != instance.text:
            analyzed_data = analyze_string(text)
            for field, value in analyzed_data.items():
                setattr(instance, field, value)

        # Update other modifiable fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
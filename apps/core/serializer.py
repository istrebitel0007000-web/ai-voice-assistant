from rest_framework import serializers


class Serializer(serializers.Serializer):
    """
    Base serializer for all project serializers.
    Returns an immutable dictionary from validated_data.
    All serializers in this project must inherit from this class.
    Never use ModelSerializer or bare rest_framework.serializers.Serializer.
    """

    def to_internal_value(self, data):
        result = super().to_internal_value(data)
        return result

    @property
    def validated_data(self):
        data = super().validated_data
        return dict(data)

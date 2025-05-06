from rest_framework import serializers
from .models import WorkItemModel


class WorkItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkItemModel
        fields = "__all__"

    def validate_detail(self, value):
        expected_keys = {
            'work_item',
            # todo adding more in future
        }
        if not isinstance(value, dict):
            raise serializers.ValidationError("Detail must be dictionary")

        for key, value in value.items():
            if not isinstance(key, str) or not isinstance(value, str):
                raise serializers.ValidationError(f" both key {key}, value {value} must be string")
        return value

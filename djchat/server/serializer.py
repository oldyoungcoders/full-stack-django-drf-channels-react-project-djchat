from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = "__all__"


class ServerSerializer(serializers.ModelSerializer):
    num_members = serializers.SerializerMethodField()
    channel_server = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ("member",)
        # fields = "__all__"

    def get_num_members(self, obj):
        if hasattr(obj, "num_members"):
            return obj.num_members
        else:
            return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        num_members = self.context.get("number_members")
        if not num_members:
            data.pop("num_members", None)

        return data

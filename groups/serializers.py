from rest_framework import serializers
from .models import Membership, Group
from users.models import User
from users.serializers import UserSerializer

class MemberSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    user = UserSerializer(required=False, read_only=True)
    user_id = serializers.IntegerField(required=False, write_only=True)
    group_id = serializers.IntegerField(write_only=True)
    role = serializers.IntegerField(required=False)
    can_assign_tasks = serializers.BooleanField(required=False)
    can_add_members = serializers.BooleanField(required=False)
    can_edit_group = serializers.BooleanField(required=False)

    def validate(self, data):
        if "user_id" not in data and "email" not in data:
            raise serializers.ValidationError("user_id or email must be provided")

        return super().validate(data)
    
    def ensure_user_id_exists(self, validated_data):
        if "user_id" not in validated_data:
            user = User.objects.get(email=validated_data.pop("email"))
            validated_data["user_id"] = user.id
    
    def create(self, validated_data):
        self.ensure_user_id_exists(validated_data)
        return Membership.objects.create(**validated_data)

    def update(self, instance, validated_data):
        self.ensure_user_id_exists(validated_data)
        instance.role = validated_data.get("role", instance.role)
        instance.can_assign_tasks = validated_data.get("can_assign_tasks", instance.can_assign_tasks)
        instance.can_add_members = validated_data.get("can_add_members", instance.can_add_members)
        instance.can_edit_group = validated_data.get("can_edit_group", instance.can_edit_group)
        instance.save()
        return instance

class MemberCreateSerializer(MemberSerializer):
    group_id = serializers.IntegerField(required=False, write_only=True)

class GroupSerializer(serializers.ModelSerializer):
    members = MemberCreateSerializer(source="membership_set", many=True)

    class Meta: 
        model = Group
        exclude = ["users"]

    def create(self, validated_data):
        members = validated_data.pop("membership_set")
        group = super().create(validated_data)
        request = self.context['request']
        
        # make the user who created the group the leader of the group
        Membership.objects.create(
            user_id=request.user.id,
            group_id=group.id,
            can_edit_group=True,
            can_add_members=True, 
            can_assign_tasks=True,
            role=Membership.Role.LEADER
        )

        # add all members to the group 
        for member in members:
            member["group_id"] = group.id
            ser = MemberSerializer(data=member)
            if(ser.is_valid()):
                ser.save()

        return group


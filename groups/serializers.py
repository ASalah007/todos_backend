from rest_framework import serializers
from .models import Membership, Group
from users.models import User

class MembershipSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=False)

    class Meta: 
        model = Membership
        fields= "__all__"
        extra_kwargs = {
            "user": {"required": False}, # can accept email instead
            "group": {"required": False} 
            
        }

    def validate(self, data):
        if "user_id" not in data and "email" not in data:
            raise serializers.ValidationError("user_id or email must be provided")

        return super().validate(data)
    
    def ensure_user_id_exists(self, validated_data):
        try: 
            if "user_id" not in validated_data:
                user = User.objects.get(email=validated_data.pop("email"))
                validated_data["user_id"] = user.id
        except User.DoesNotExist: ...
    
    def create(self, validated_data):
        self.ensure_user_id_exists(validated_data)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        self.ensure_user_id_exists(validated_data)
        return super().update(instance, validated_data)



class GroupSerializer(serializers.ModelSerializer):
    users = MembershipSerializer(required=False, many=True)

    class Meta: 
        model = Group
        fields = "__all__"

    def create(self, validated_data):
        members = validated_data.pop("users")
        group = super().create(**validated_data)
        request = self.context['request']
        
        # make the user who created the group the leader of the group
        Membership.objects.create(
            user=request.user,
            group=group,
            can_edit_group=True,
            can_add_members=True, 
            can_assign_tasks=True,
            role=Membership.Role.LEADER
        )

        # add all members to the group 
        for member in members:
            Membership.objects.create(
                group=group,
                user_id=member.get("user_id"),
                email=member.get("email"),
                role=member.get('role'),
                can_assign_tasks=member.get("can_assign_tasks"),
                can_add_members=member.get("can_add_members"), 
                can_edit_group=member.get("can_edit_group")
            )

        return group
    
    def is_valid(self, *, raise_exception=False):
        print(self.data)
        return super().is_valid(raise_exception=raise_exception)



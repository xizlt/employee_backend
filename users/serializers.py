from drf_writable_nested import WritableNestedModelSerializer
from rest_framework import serializers

from users.models import Employee, SpecialUsers, Position, Filial, AccountType, Account, Status


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = (
            'basic',
            'item',
            'password',
            'type',
            'id',
            'comment',
        )


class AccountSerializerFull(serializers.ModelSerializer):
    class Meta:
        depth = 1
        model = Account
        fields = (
            'basic',
            'item',
            'password',
            'type',
            'id',
            'comment',
        )


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('name', 'id')


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ('name', 'id')


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('name', 'id',)


class FilialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Filial
        fields = ('name', 'id')



class EmployeeSerializer(serializers.ModelSerializer):
    # account = AccountSerializer(many=True, required=False, allow_null=True)

    class Meta:
        model = Employee
        fields = (
            'id',
            'name_first',
            'name_middle',
            'name_last',
            'position',
            'comment',
            'filial',
            'status',
            'account',
        )


class EmployeeSerializerFull(WritableNestedModelSerializer, serializers.ModelSerializer):

    class Meta:
        depth = 2
        model = Employee
        fields = (
            'id',
            'name_first',
            'name_middle',
            'name_last',
            'position',
            'comment',
            'filial',
            'status',
            'account',
            'update',
            'created',
        )


class SpecialUsersSerializerFull(serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = SpecialUsers
        fields = (
            'id',
            'name',
            'comment',
            'appointment',
            'account',
            'update',
            'created'
        )


class SpecialUsersSerializer(WritableNestedModelSerializer, serializers.ModelSerializer):
    account = AccountSerializer()

    class Meta:
        model = SpecialUsers
        fields = (
            'id',
            'name',
            'comment',
            'appointment',
            'account',
        )

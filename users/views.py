import re

import unicodecsv as csv
from django.shortcuts import render

from django.http import JsonResponse, HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.forms import CreatePassword, validation
from users.models import Employee, SpecialUsers, Position, Filial, AccountType, Account, Status
from users.serializers import EmployeeSerializer, SpecialUsersSerializer, PositionSerializer, FilialSerializer, \
    AccountTypeSerializer, AccountSerializer, StatusSerializer, EmployeeSerializerFull, SpecialUsersSerializerFull, \
    AccountSerializerFull
from users.service import password_generator


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects. \
        select_related('filial',
                       'status',
                       ). \
        prefetch_related('position',
                         'account',
                         'account__type',
                         ).all()
    serializer_class = EmployeeSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    # pagination_class = LimitOffsetPagination
    search_fields = ['name_last',
                     'name_first',
                     'filial__name',
                     'account__item',
                     'position__name',
                     ]
    ordering_fields = ['name_last',
                       'position__name',
                       'filial__name',
                       'account__item',
                       'status__name',
                       ]

    action_to_serializer = {
        "list":     EmployeeSerializerFull,
        "retrieve": EmployeeSerializerFull,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class SpecialUsersViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = SpecialUsers.objects.select_related("account").all()
    serializer_class = SpecialUsersSerializer
    permission_classes = [permissions.IsAdminUser]
    # pagination_class = LimitOffsetPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['item']
    ordering_fields = ['item',
                       'basic',
                       'type',
                       ]

    action_to_serializer = {
        "list":     SpecialUsersSerializerFull,
        "retrieve": SpecialUsersSerializerFull,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class PositionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAdminUser]


class FilialViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Filial.objects.all()
    serializer_class = FilialSerializer
    permission_classes = [permissions.IsAdminUser]


# /api/v1/create_password?len=6&ti=true&tl=true&tp=false&account=5
@api_view(('GET',))
@permission_classes((permissions.IsAdminUser,))
@validation(CreatePassword)
def create_password(request, valid_data):
    ti = valid_data.get('ti')
    tl = valid_data.get('tl')
    tp = valid_data.get('tp')
    try:
        return JsonResponse({"status":   True,
                             "password": password_generator(length=valid_data.get('length'), cbl=[ti, tl, tp])
                             })
    except Exception as err:
        return JsonResponse({"status": False,
                             "error":  err.__str__()
                             })


class AccountTypeViewSet(viewsets.ModelViewSet):
    queryset = AccountType.objects.all()
    serializer_class = AccountTypeSerializer
    permission_classes = [permissions.IsAdminUser]


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.select_related('type').all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAdminUser]
    pagination_class = LimitOffsetPagination

    action_to_serializer = {
        "list":     AccountSerializerFull,
        "retrieve": AccountSerializerFull,
    }

    def get_serializer_class(self):
        return self.action_to_serializer.get(
            self.action,
            self.serializer_class
        )


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer
    permission_classes = [permissions.IsAdminUser]


@api_view(('GET',))
@permission_classes((permissions.IsAdminUser,))
def create_template(request):
    """
    Template for email with accounts information.
    """
    user_id = request.GET.get('user_id')
    user = Employee.objects.get(pk=user_id)
    accounts = Account.objects.filter(employee=user_id, basic=True)

    text_template = ""
    for account in accounts:
        if account.type.id == 1:
            text_template += f"внутренний номер:/n{account.item}/n"
        if account.type.id == 2:
            text_template += f"почтовый ящик: {account.item}/nпароль: {account.password}/n"
        if account.type.id == 3:
            text_template += f"Сотрудник: {user.full_name()}/nПользователь: {account.item}/nпароль: {account.password}"
    return JsonResponse({"result": text_template})


@api_view(('GET',))
@permission_classes((permissions.IsAdminUser,))
def get_csv_for_accounts(request, temp):
    templates_csv = ('account', 'free',)
    name = templates_csv[0]

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{name}.csv"'
    writer = csv.writer(response, delimiter=",", encoding="utf-8-sig")

    if temp == 'account':
        for employee in Employee.objects.filter():

            writer.writerow([
                f"CN={employee.full_name()},OU=Contacts,DC=electro,DC=local",
                "contact",
                '',
                f"CN={employee.full_name()},OU=Contacts,DC=electro,DC=local",
                employee.full_name(),
                "CN=Person,CN=Schema,CN=Configuration,DC=electro,DC=local",
                employee.full_name(),
                employee.name_last,
                employee.get_main_phone_number(),
                employee.name_first,
                employee.filial.name,
                employee.filial.name,
                employee.get_main_email(),
            ])
    elif temp == 'free':
        # TODO ?
        pass

    return response


@api_view(('POST',))
@permission_classes((permissions.IsAdminUser,))
def black_list_refresh_view(request):
    token = RefreshToken(request.data.get('refresh_token'))
    token.blacklist()
    return Response("Successful Logout", status=status.HTTP_200_OK)

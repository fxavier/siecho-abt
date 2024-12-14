import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth import authenticate
from graphql import GraphQLError
from datetime import datetime
from user.models import User
from app.authentication import TokenManager
from app.permissions import is_authenticated, paginate


class UserType(DjangoObjectType):
    class Meta:
        model = User


class Query(graphene.ObjectType):
    users = graphene.Field(paginate(UserType), page=graphene.Int())
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.filter(**kwargs)

    @is_authenticated
    def resolve_user(self, info, id):
        return User.objects.get(pk=id)

    @is_authenticated
    def resolve_me(self, info):
        user = info.context.user
        return user


class RegisterUser(graphene.Mutation):
    status = graphene.Boolean()
    message = graphene.String()

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        first_name = graphene.String()
        last_name = graphene.String()

    def mutate(self, info, email, password):
        User.objects.create_user(email, password)

        return RegisterUser(
            status=True,
            message="User Created successfully"
        )


class LoginUser(graphene.Mutation):
    access = graphene.String()
    refresh = graphene.String()
    user = graphene.Field(UserType)

    class Arguments:
        email = graphene.String(required=True)
        password = graphene.String(required=True)

    def mutate(self, info, email, password):
        user = authenticate(username=email, password=password)

        if not user:
            raise Exception("invalid credentials")

        user.last_login = datetime.now()
        user.save()

        access = TokenManager.get_access({"user_id": user.id})
        refresh = TokenManager.get_refresh({"user_id": user.id})

        return LoginUser(
            access=access,
            refresh=refresh,
            user=user
        )


class GetAccess(graphene.Mutation):
    access = graphene.String()

    class Arguments:
        refresh = graphene.String(required=True)

    def mutate(self, info, refresh):
        token = TokenManager.decode_token(refresh)

        if not token or token["type"] != "refresh":
            raise Exception("Invalid token or has expired")

        access = TokenManager.get_access({"user_id": token["user_id"]})

        return GetAccess(
            access=access
        )


class Mutation(graphene.ObjectType):
    register_user = RegisterUser.Field()
    login_user = LoginUser.Field()
    get_access = GetAccess.Field()

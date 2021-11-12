import graphene
from django.contrib.auth.models import User
from graphene import Field, ObjectType, Schema
from graphene import Mutation, String
from graphene_django import DjangoObjectType
from graphql_jwt import ObtainJSONWebToken, Verify, Refresh
from graphql_jwt.decorators import login_required

from todo.models import Todo
from todo.schema import TodoType


class UserType(DjangoObjectType):
    class Meta:
        model = User
        exclude = ('password',)


class UserCreate(Mutation):
    user = Field(UserType)

    class Arguments:
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)

    def mutate(self, info, username, password, email):
        user = User(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return UserCreate(user=user)


class UserCreateTodo(Mutation):
    todo = Field(TodoType)

    class Arguments:
        title = String(required=True)

    @login_required
    def mutate(self, info, title):
        user = info.context.user
        todo = Todo.objects.create(title=title, user=user)
        return UserCreateTodo(todo=todo)


class UserUpdateTodoState(Mutation):
    todo = Field(TodoType)

    class Arguments:
        id = graphene.Int(required=True)
        state = graphene.String(required=True)

    @login_required
    def mutate(self, info, id, state):
        user = info.context.user
        todo = user.todo_set.get(pk=id)
        if todo:
            todo.state = state
            todo.save()
        return UserUpdateTodoState(todo=todo)


class UserDeleteTodo(Mutation):
    todo = Field(TodoType)

    class Arguments:
        id = graphene.Int(required=True)

    @login_required
    def mutate(self, info, id):
        user = info.context.user
        todo = user.todo_set.get(pk=id)
        if todo:
            todo.delete()
        return UserDeleteTodo(todo=todo)


class Query(ObjectType):
    current_user = Field(UserType)
    users = graphene.List(UserType)
    user_todos = graphene.List(TodoType)

    def resolve_users(root, info):
        return User.objects.all()

    @login_required
    def resolve_user_todos(root, info):
        user = info.context.user
        return user.todo_set.all()

    @login_required
    def resolve_current_user(root, info):
        user = info.context.user
        return user


class Mutation(ObjectType):
    user_create = UserCreate.Field()
    token_auth = ObtainJSONWebToken.Field()
    verify_token = Verify.Field()
    refresh_token = Refresh.Field()
    user_create_todo = UserCreateTodo.Field()
    user_update_todo_state = UserUpdateTodoState.Field()
    user_delete_todo = UserDeleteTodo.Field()


schema = Schema(query=Query, mutation=Mutation)

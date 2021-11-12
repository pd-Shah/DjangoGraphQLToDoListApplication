import graphene
# cookbook/ingredients/schema.py
from graphene import relay, ObjectType
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo
        filter_fields = {
            'title': ['exact', 'icontains', ],
            'state': ['exact'],
            'due_date': ['exact'],
        }
        interfaces = (relay.Node,)


class Query(ObjectType):
    todo = relay.Node.Field(TodoType)
    todos = DjangoFilterConnectionField(TodoType)


class TodoInput(graphene.InputObjectType):
    id = graphene.ID()
    title = graphene.String()
    user_id = graphene.ID()
    state = graphene.String()


class CreateTodo(graphene.Mutation):
    class Arguments:
        input = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, input=None):
        ok = True
        todo = Todo(title=input.title, user_id=input.user_id)
        todo.save()
        return CreateTodo(ok=ok, todo=todo)


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        todo = Todo.objects.get(pk=id)
        if todo:
            ok = True
            todo.title = input.title
            todo.save()
            return UpdateTodo(ok=ok, todo=todo)
        return UpdateTodo(ok=ok, todo=None)


class UpdateTodoState(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        todo = Todo.objects.get(pk=id)
        if todo:
            ok = True
            todo.state = input.state
            todo.save()
            return UpdateTodoState(ok=ok, todo=todo)
        return UpdateTodoState(ok=ok, todo=None)


class UpdateTodoDueDate(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)
        input = TodoInput(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        todo = Todo.objects.get(pk=id)
        if todo:
            ok = True
            todo.due_date = input.due_date
            todo.save()
            return UpdateTodoDueDate(ok=ok, todo=todo)
        return UpdateTodoDueDate(ok=ok, todo=None)


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()
    todo = graphene.Field(TodoType)

    @staticmethod
    def mutate(root, info, id, input=None):
        ok = False
        todo = Todo.objects.get(pk=id)
        if todo:
            ok = True
            todo.delete()
            return DeleteTodo(ok=ok, todo=todo)
        return DeleteTodo(ok=ok, todo=None)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    update_todo_state = UpdateTodoState.Field()
    delete_todo = DeleteTodo.Field()
    update_todo_due_date = UpdateTodoDueDate.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

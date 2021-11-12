import graphene

from todo.schema import Mutation as TodoMutation
from todo.schema import Query as TodoQuery
from user.schema import Mutation as UserMutation
from user.schema import Query as UserQuery


class Query(TodoQuery, UserQuery, graphene.ObjectType):
    pass


class Mutation(TodoMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)

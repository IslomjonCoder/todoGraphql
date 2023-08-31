# todoapp/schema.py
import graphene
from graphene_django.types import DjangoObjectType

from .models import Todo


class TodoType(DjangoObjectType):
    class Meta:
        model = Todo


class Query(graphene.ObjectType):
    all_todos = graphene.List(TodoType)

    def resolve_all_todos(self, info):
        return Todo.objects.all()


schema = graphene.Schema(query=Query)


# todoapp/schema.py
# ...

class CreateTodo(graphene.Mutation):
    class Arguments:
        title = graphene.String()
        description = graphene.String()

    todo = graphene.Field(TodoType)

    def mutate(self, info, title, description=None):
        todo = Todo(title=title, description=description)
        todo.save()
        return CreateTodo(todo=todo)


class UpdateTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
        completed = graphene.Boolean()

    todo = graphene.Field(TodoType)

    def mutate(self, info, id, title=None, description=None, completed=None):
        try:
            todo = Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            raise Exception("Todo not found")

        if title is not None:
            todo.title = title
        if description is not None:
            todo.description = description
        if completed is not None:
            todo.completed = completed

        todo.save()
        return UpdateTodo(todo=todo)


class DeleteTodo(graphene.Mutation):
    class Arguments:
        id = graphene.ID()

    success = graphene.Boolean()

    def mutate(self, info, id):
        try:
            todo = Todo.objects.get(pk=id)
        except Todo.DoesNotExist:
            raise Exception("Todo not found")

        todo.delete()
        return DeleteTodo(success=True)


class Mutation(graphene.ObjectType):
    create_todo = CreateTodo.Field()
    update_todo = UpdateTodo.Field()
    delete_todo = DeleteTodo.Field()


schema = graphene.Schema(query=Query, mutation=Mutation)

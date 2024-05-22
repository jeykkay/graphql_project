import graphene
from graphene import ObjectType
from graphene_django import DjangoObjectType
from books.models import Book


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        published_year = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, published_year):
        book = Book(title=title, author=author, published_year=published_year)
        book.save()
        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)
        title = graphene.String()
        author = graphene.String()
        published_year = graphene.Int()

    book = graphene.Field(BookType)

    def mutate(self, info, id, title, author, published_year):
        book = Book.objects.get(id=id)
        if title:
            book.title = title
        if author:
            book.author = author
        if published_year:
            book.published_year = published_year
        book.save()
        return UpdateBook(book=book)


class DeleteBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    success = graphene.Boolean()

    def mutate(self, info, id):
        book = Book.objects.get(pk=id)
        book.delete()
        return DeleteBook(success=True)


class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
    delete_book = DeleteBook.Field()


class Query(graphene.ObjectType):
    book = graphene.Field(BookType, id=graphene.ID())
    all_books = graphene.List(BookType)

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_all_books(self, info):
        return Book.objects.all()


schema = graphene.Schema(query=Query, mutation=Mutation)

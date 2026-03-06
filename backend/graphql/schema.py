import strawberry
from backend.graphql.queries import Query
from backend.graphql.mutations import Mutation


schema = strawberry.Schema(
    query=Query,
    mutation=Mutation
)
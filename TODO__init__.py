#TODO: create uniqueness constraint in DB
#http://nicolewhite.github.io/neo4j-flask/pages/the-data-model.html
# from .views import app
# from .models import graph
#
# def create_uniqueness_constraint(label, property):
#     query = "CREATE CONSTRAINT ON (n:{label}) ASSERT n.{property} IS UNIQUE"
#     query = query.format(label=label, property=property)
#     graph.cypher.execute(query)
#
# create_uniqueness_constraint("User", "username")
# create_uniqueness_constraint("Tag", "name")
# create_uniqueness_constraint("Post", "id")
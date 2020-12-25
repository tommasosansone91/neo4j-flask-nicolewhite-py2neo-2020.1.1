from .views import app
from .models import graph

# graph.run("CREATE CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")
# graph.run("CREATE CONSTRAINT ON (n:Post) ASSERT n.id IS UNIQUE")
# graph.run("CREATE CONSTRAINT ON (n:Tag) ASSERT n.name IS UNIQUE")
# graph.run("CREATE INDEX ON :Post(date)")
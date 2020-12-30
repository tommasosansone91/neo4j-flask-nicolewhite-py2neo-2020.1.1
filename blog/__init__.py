from .views import app
from .models import graph



try:
    graph.run("CREATE CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")
except:
    print("Fallita creazione indice: CREATE CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")



try:
    graph.run("CREATE CONSTRAINT ON (n:Post) ASSERT n.id IS UNIQUE")
except:
    print("Fallita creazione indice: CREATE CONSTRAINT ON (n:Post) ASSERT n.id IS UNIQUE")


try:
    graph.run("CREATE CONSTRAINT ON (n:Tag) ASSERT n.name IS UNIQUE")
except:
    print("Fallita creazione indice: CREATE CONSTRAINT ON (n:Tag) ASSERT n.name IS UNIQUE")


try:
    graph.run("CREATE INDEX ON :Post(date)")
except:
    print("Fallita creazione indice: CREATE INDEX ON :Post(date)")

# graph.run("CREATE CONSTRAINT ON (n:User) ASSERT n.username IS UNIQUE")
# graph.run("CREATE CONSTRAINT ON (n:Post) ASSERT n.id IS UNIQUE")
# graph.run("CREATE CONSTRAINT ON (n:Tag) ASSERT n.name IS UNIQUE")
# graph.run("CREATE INDEX ON :Post(date)")
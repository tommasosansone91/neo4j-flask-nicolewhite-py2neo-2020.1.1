from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
from datetime import datetime
import uuid


# graph = Graph()

graph = Graph("bolt://localhost:7687", user="neo4j", password="Neo4j")

class User:

    def __init__(self, username):
        self.username = username

    def find(self):

        # Find one node (and take only one if there are many) matching these conditions: its type is "Person" and it has an attribute "name" equal to "Kenny", and then save it inside "kenny" variable.
        matcher = NodeMatcher(graph)
        user = matcher.match('User', username=self.username).first()
        return user

    def register(self, password):
        if not self.find():
            user = Node("User", username=self.username, password=bcrypt.encrypt(password))
            # con questo evito di sotrare le password raw, rpima le critto
            
            graph.create(user)
            return True
        return False

    def verify_password(self, password):
        user = self.find()

        if not user:
            return False

        return bcrypt.verify(password, user["password"])

    def add_post(self, title, tags, text):
        user = self.find()

        time_now = datetime.now()

        post = Node(
            "Post",
            id = str(uuid.uuid4()),
            title=title,
            text=text,
            timestamp = int(time_now.strftime("%S")),
            date=time_now.strftime("%F")

        )    
 

        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)

        

        try:
            tags = [x for x in tags.lower().split(", ")]
            print("L'utente ha inserito i tag separati da virgola e spazio.")
        except:
            pass

        try:
            tags = [x for x in tags.lower().split(",")]
            print("L'utente ha inserito i tag separati da virgola.")
        except:
            pass


        print(tags)
        tags = set(tags) # evita che sia creato 2 volte lo stesso tag

        for tag in tags:
            tag_node = Node("Tag", name=tag)
            tag_node.__primarylabel__ = list(tag_node.labels)[0]
            tag_node.__primarykey__ = "name"
            graph.merge(tag_node)

            rel = Relationship(tag_node, "TAGGED", post)
            graph.create(rel)

    def like_post(self, post_id):
        user = self.find()

        matcher = NodeMatcher(graph)
        post = matcher.match("Post", id=post_id).first()

        rel = Relationship(user, "LIKES", post)
        graph.merge(rel)


def todays_recent_posts(n):
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date = $today
    RETURN user.username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT $n
    """
    
    today = datetime.now().strftime("%F")
    return graph.run(query, today=today, n=n)


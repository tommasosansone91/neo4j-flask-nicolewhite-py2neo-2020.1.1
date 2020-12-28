from py2neo import Graph, Node, Relationship, NodeMatcher
from passlib.hash import bcrypt
from datetime import datetime, timedelta
import uuid
import os

from .auxiliary_functions import gregorian_calendar



url = os.environ.get("GRAPHENEDB_URL", "http://localhost:7687")

graph = Graph(url + "/db/data/")

# graph = Graph("bolt://localhost:7687", user="neo4j", password="Neo4j")

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
            timestamp = int( datetime.timestamp(time_now) ),
            date=time_now.strftime("%F")

        )    
 


        rel = Relationship(user, "PUBLISHED", post)
        graph.create(rel)


        gregorian_calendar(graph, time1=time_now, node1=post)


        # ahndle tags separated by both ", " and ","
        tags = tags.replace(", ", ",")
        tags = tags.replace(" ,", ",")
            
        try:
            tags = [x for x in tags.lower().split(",")]
        except:
            pass


        # print(tags)
        tags = set(tags) # evita che sia creato 2 volte lo stesso tag

        for tag in tags:
            tag_node = Node("Tag", name=tag)
            tag_node.__primarylabel__ = list(tag_node.labels)[0] #banalmente la primary abel è la prima delle label
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

    def recent_posts(self, n):
        query = """
        MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
        WHERE user.username = $username
        RETURN post, COLLECT(tag.name) AS tags
        ORDER BY post.timestamp DESC LIMIT $n
        """
        return graph.run(query, username=self.username, n=n)

    def similar_users(self, n):
        query = """
        MATCH (user1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (user2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE user1.username = $username AND user1 <> user2
        WITH user2, COLLECT(DISTINCT tag.name) AS tags, COUNT(DISTINCT tag.name) AS tag_count
        ORDER BY tag_count DESC LIMIT $n
        RETURN user2.username AS similar_user, tags
        """
        return graph.run(query, username=self.username, n=n)

    def commonality_of_user(self, user):

        query1 = """
        MATCH (user1:User)-[:PUBLISHED]->(post:Post)<-[:LIKES]-(user2:User)
        WHERE user1.username = $username1 AND user2.username = $username2
        RETURN COUNT(post) AS likes
        """

        likes = graph.run(query1, username1=self.username, username2=user.username).data()[0]["likes"]
        likes = 0 if not likes else likes
        print(likes)

        query2 = """
        MATCH (user1:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag:Tag),
              (user2:User)-[:PUBLISHED]->(:Post)<-[:TAGGED]-(tag)
        WHERE user1.username = $username1 AND user2.username = $username2 
        RETURN COLLECT(DISTINCT tag.name) AS tags 
        """

        


        tags = graph.run(query2, username1=self.username, username2=user.username).data()[0]["tags"]
        print(tags)

        return {"likes":likes, "tags":tags}   
        # return {"likes":likes, "common":tags} 


def todays_recent_posts(n):
    query = """
    MATCH (user:User)-[:PUBLISHED]->(post:Post)<-[:TAGGED]-(tag:Tag)
    WHERE post.date >= $date1
    RETURN user.username AS username, post, COLLECT(tag.name) AS tags
    ORDER BY post.timestamp DESC LIMIT $n
    """
    
    today = datetime.now()
    delta = timedelta(days = 5) # days
    date1 = today - delta
    date1 = date1.strftime("%F")

    return graph.run(query, date1=date1, n=n)



from py2neo import Graph, Node, Relationship
from datetime import datetime



# similar to https://py2neo.org/v3/_modules/py2neo/ext/calendar/gregorian.html
def gregorian_calendar(graph, time1=None, node1=None):

    if time1 is None:
        time1 = datetime.now()

    # gregorian calendar node
    gregorian_node = Node("Calendar", calendar_type="Gregorian")
    gregorian_node.__primarylabel__ = list(gregorian_node.labels)[0]
    gregorian_node.__primarykey__ = "calendar_type"
    graph.merge(gregorian_node)

    # year node
    that_year_node = Node("Year", year=time1.year, key=time1.strftime("%Y"))
    that_year_node.__primarylabel__ = list(that_year_node.labels)[0]
    that_year_node.__primarykey__ = "year"
    graph.merge(that_year_node)

    # calendar has year
    rel = Relationship(gregorian_node, "YEAR", that_year_node)
    graph.merge(rel)

    # month node
    that_month_node = Node("Month", month=time1.month, key=time1.strftime("%m-%Y"))
    that_month_node.__primarylabel__ = list(that_month_node.labels)[0]
    that_month_node.__primarykey__ = "month"
    graph.merge(that_month_node)

    # year has month
    rel = Relationship(that_year_node, "MONTH", that_month_node)
    graph.merge(rel)

    # day node
    that_day_node = Node("Day", day=time1.day, key=time1.strftime("%d-%m-%Y"))
    that_day_node.__primarylabel__ = list(that_day_node.labels)[0]
    that_day_node.__primarykey__ = "day"
    graph.merge(that_day_node)

    # month has day
    rel = Relationship(that_month_node, "DAY", that_day_node)
    graph.merge(rel)

    # post was published on (gregorian) day
    if node1 is not None:
        rel = Relationship(node1, "ON", that_day_node)
        graph.create(rel)
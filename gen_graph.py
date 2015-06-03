import sys
import os
import re
from os import listdir
from os.path import isfile, join
from peewee import *
from gexf import *

db = SqliteDatabase('sou.db')


class SOU(Model):
    name = TextField()
    number = CharField(unique=True)
    length = IntegerField()

    class Meta:
        database = db


class Relation(Model):
    fromsou = ForeignKeyField(SOU, related_name='relations')
    tosou = ForeignKeyField(SOU, related_name='inrelations')

    class Meta:
        database = db


if __name__ == '__main__':

    destination_file = sys.argv[1] #e.g. result.gexf
    print "Writing to %s" % destination_file

    gexf = Gexf("KB","SOU-relationer")
    graph=gexf.addGraph("directed","static","SOU-grafen")
    graph.addNodeAttribute(title="name", defaultValue=None, type="string")
    graph.addNodeAttribute(title="number", defaultValue=None, type="string")
    graph.addNodeAttribute(title="length", defaultValue=None, type="integer")

    for sou in SOU.select():
       n = graph.addNode(sou.number, sou.number)
       #n.addAttribute("name", sou.name)
       #n.addAttribute("length", sou.length)
       #n.addAttribute("number", sou.number)


    for edge in Relation.select():
        graph.addEdge(edge.id, edge.fromsou.number, edge.tosou.number)

    output_file=open(destination_file,"w")
    gexf.write(output_file)



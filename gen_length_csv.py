import sys
import traceback
import os
import re
from os import listdir
from os.path import isfile, join
from peewee import *
import collections

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

    data = collections.OrderedDict()

    for sou in SOU.select().order_by(SOU.number):
        year = sou.number.split(":")[0]
        if not data.has_key(year):
            data[year] = 0

        data[year] += 1 # or sou.length

    for k, v in data.items():
        print "%s, %s" % (k,v)


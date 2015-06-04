# -*- coding: utf-8 -*-
import sys
import os
import re
from os import listdir
from os.path import isfile, join
from peewee import *


REGEX = re.compile(ur'SOU (\d\d\d\d\:\d+\w?)', re.MULTILINE)


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


def parse_refs(filename, sou):

    text = ""

    with open(filename, 'r') as f:
        text = f.read()

    # parse refs
    refs = re.findall(REGEX, text)

    for ref in refs:
        if ref != sou.number:
            print "%s ---> %s" % (current_sou, ref)
            target_sou = SOU.get(SOU.number == ref)
            relation = Relation(fromsou = sou, tosou=target_sou)
            relation.save()



def parse_souno_from_filename(filename):
    year = re.match(".*SOU (\d\d\d\d)\:(\d+)\.", filename).group(1)
    no = re.match(".*SOU (\d\d\d\d)\:(\d+)\.", filename).group(2)
    return "%s:%s" % (year, no)



if __name__ == '__main__':

    db.create_tables([SOU, Relation], safe=True)

    folder = sys.argv[1] # abspath
    print "Working on %s" % folder

    # iterate over files
    for d in listdir(folder):
        if not isfile(join(folder,d)):
            for f in listdir(join(folder,d)):
                if isfile(join(folder,d,f)):
                    if f.endswith(".txt"):

                        try:
                            #get current SOU number
                            current_sou = parse_souno_from_filename(f)
                            sou = SOU.get(SOU.number == current_sou)

                            parse_refs(join(folder,d,f), sou)

                        except:
                            print "Skipping %s" % f

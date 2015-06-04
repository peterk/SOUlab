import sys
import os
import re
from os import listdir
from os.path import isfile, join
from peewee import *

db = SqliteDatabase('sou.db')

class SOU(Model):
    name = TextField()
    number = CharField(unique=True)
    length = IntegerField()

    class Meta:
        database = db


class Relation(Model):
    fromsou = ForeignKeyField(SOU, related_name='references')
    tosou = ForeignKeyField(SOU, related_name='inreferences')

    class Meta:
        database = db


def parse_souno_from_filename(filename):
    year = re.match(".*SOU (\d\d\d\d)\:(\d+\w?)\.", filename).group(1)
    no = re.match(".*SOU (\d\d\d\d)\:(\d+\w?)\.", filename).group(2)
    return "%s:%s" % (year, no)

def parse_name(filename):
    return filename.replace(".txt","")

if __name__ == '__main__':

    db.create_tables([SOU, Relation], safe=True)

    folder = sys.argv[1] # root folder for txt files. Expecting e.g. <root>/20tal/<soufile>.txt
    print "Working on %s" % folder

    for d in listdir(folder):
        if not isfile(join(folder,d)):
            for f in listdir(join(folder,d)):
                if isfile(join(folder,d,f)):
                    if f.endswith(".txt"):
                        try:
                            if not "Bilagedel" in f and not "Bilaga" in f and not "Bilagor" in f and not "bilaga" in f and not "bilagor" in f:
                                current_sou = parse_souno_from_filename(f)
                                length = os.path.getsize(join(folder,d,f))
                                name = parse_name(f)

                                sou = SOU(name=name, length=length, number=current_sou)
                                result = sou.save()
                        except:
                            print "---> Skipped %s" % f
                            pass


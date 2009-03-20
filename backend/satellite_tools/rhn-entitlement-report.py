#!/usr/bin/python

import sys
import getopt
from pprint import pprint

sys.path.append('/usr/share/rhn')
try:
   from server import rhnSQL
   from common import initCFG, CFG
except:
   print "Couldn't load needed libs, Are you sure you are running this on a satellite?"
   sys.exit(1)



initCFG()
db_string = CFG.DEFAULT_DB
rhnSQL.initDB(db_string)

def main():
    list = listOfOrgs()
    for org in list:
       printOrgHeader(org);
       printSystemEnts(org['id']);
       printChannelEnts(org['id']);
    printOrgFooter()


def printOrgHeader(org):
   print("\n")
   print("="*40)
   print(org['name'] + " (" + str(org['id']) + "):\n")


def printOrgFooter():
   print("="*40)
   print("\n")


def printChannelEnts(id):
   query = "select CF.label, PCF.current_members from rhnChannelFamily CF inner join rhnPrivateChannelFamily PCF on CF.id = PCF.channel_family_id where PCF.org_id = %d order by CF.label" % (id)
   list = run_query(query)
   print("%35s %s" % ("Channel Entitelment", "Used"))
   print("%35s %s" % ("-------------------", "----"))
   if list == None:
      print("")
      return
   for item in list:
      if item['current_members'] != 0:
         print("%35s %s" % (item['label'], str(item['current_members'])))
   print("")
   return

def printSystemEnts(id):
   print("%35s %s" % ("System Entitelment", "Used"))
   print("%35s %s" % ("------------------", "----"))
   query = """select T.label, G.current_members
                 from rhnServerGroup G inner join rhnServerGroupType T  on G.group_type = T.id
		 where org_id = %d order by T.label """ % (id)
   list = run_query(query)
   for item in list:
         print("%35s %s" % (item['label'], str(item['current_members'])))
   print("")
   return



def listOfOrgs():
   query = "select id, name from web_customer"
   return run_query(query)

def run_query(query):
   _get_data_sql = rhnSQL.prepare(query)
   _get_data_sql.execute()
   return _get_data_sql.fetchall_dict()



if __name__ == "__main__":
    main()




#!/usr/bin/python

import sys
import mysql.connector
from mysql.connector import Error
import json
from json import JSONEncoder
import datetime


class DateTimeEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return str(int((obj - datetime.datetime(1970, 1, 1)).total_seconds()))


username = sys.argv[1]
op = str(sys.argv[2])

project = None
profilename = None
if len(sys.argv) > 4:
    project = sys.argv[3]
    profilename = sys.argv[4]

try:
    connection = mysql.connector.connect(host='localhost',
                                         database='tbdb',
                                         user='mysql',
                                         password='',
                                         unix_socket='/tmp/mysql.sock')
    cursor = connection.cursor()
    if op == "list_experiments":
        list_experiment_query = 'select uuid, name, pid, profile_id, profile_version, aggregate_urn, started, status from apt_instances where creator = "{}";'.format(
            username)
        cursor.execute(list_experiment_query)
        records = cursor.fetchall()

        experiments = []
        for row in records:
            cursor2 = connection.cursor()

            cursor2.execute(
                'select pid, name from apt_profile_versions where profileid = {};'.format(row[3]))
            profile = cursor2.fetchall()
            cursor2.close()
            profile_string = profile[0][0] + ',' + profile[0][1]
            dict_r = {'username': username,
                      'uuid': row[0],       # uuid
                      'name': row[1],       # name
                      'project': row[2],    # pid
                      'profile': profile_string,  # profile_proj, profile_name
                      'profile_version': row[4],  # profile_version
                      'cluster': row[5],    # aggregate_urn
                      'start': row[6],      # started (datetime)
                      'status': row[7]}     # status

            experiments.append(dict_r)
        print(json.dumps(experiments, cls=DateTimeEncoder))

    elif op == "list_profiles":
        query = 'select name, pid, version, created, rspec, script, uuid from apt_profile_versions where creator="{}" and deleted IS NULL;'.format(
            username)
        cursor.execute(query)
        records = cursor.fetchall()

        profiles = []
        for row in records:
            dict_r = {'creator': username,
                      'name': row[0],     # name
                      'project': row[1],  # pid
                      'version': row[2],  # version
                      'created': row[3],  # created
                      'rspec': row[4],  # repourl
                      'script': row[5],  # script
                      'uuid': row[6]}  # uuid
            profiles.append(dict_r)
        print(json.dumps(profiles, cls=DateTimeEncoder))

    elif op == "query_profile":
        query = 'select name, pid, version, created, rspec, script, uuid from apt_profile_versions where creator="{}" and pid="{}" and name="{}" and deleted IS NULL;'.format(
            username,
            project,
            profilename)
        cursor.execute(query)
        records = cursor.fetchall()

        profiles = []
        for row in records:
            dict_r = {'creator': username,
                      'name': row[0],     # name
                      'project': row[1],  # pid
                      'version': row[2],  # version
                      'created': row[3],  # created
                      'rspec': row[4],  # repourl
                      'script': row[5],  # script
                      'uuid': row[6]}  # uuid
            profiles.append(dict_r)
        print(json.dumps(profiles, cls=DateTimeEncoder))

except Error as e:
    print("Error: ", e)
finally:
    if connection.is_connected():
        connection.close()
        cursor.close()

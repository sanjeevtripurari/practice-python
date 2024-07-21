# kafka-consumer

from    kafka import KafkaConsumer
from    json import loads
from    datetime import datetime
import  psycopg2

consumer = KafkaConsumer(
        'test',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='my-group',
        value_deserializer=lambda x: loads(x.decode('utf-8'))
        )
"""
for message in consumer:
    messager = message.value
#    print('messageR: {}'.format(messager))
    print('message.last_updated: {}'.format(messager['last_updated']))
#    print('message.date: {}'.format(messager['data']))
    for station in messager['data']['stations']:
        print ("station: {}".format(station))
        print("Station_id: {}".format(station['station_id']))
        break
    break
exit
"""
conn=psycopg2.connect(database="oslo_city_bike", user='root',password='secret', host='127.0.0.1', port='5432')
cursor = conn.cursor()

for message in consumer:
    messager          = message.value
    timestamp         = messager['last_updated']
    dt_object         = datetime.fromtimestamp(timestamp)
    messager['Date']  = dt_object.strftime("%b %d %Y %H:%M:%S")
    datehrs           = dt_object.strftime("%b %d %Y %H:%M:%S")
    for station in messager['data']['stations']:
        _station_id=station['station_id']
        _station_is_installed=station['is_installed']
        _station_is_renting=station['is_renting']
        _station_is_returning=station['is_returning']
        _station_last_reported=station['last_reported']
        _station_num_vehicles_available=station['num_vehicles_available']
        _station_num_bikes_available=station['num_bikes_available']
        _station_num_docks_available=station['num_docks_available']

        cursor.execute("INSERT INTO Station_Status ( Station_id, is_installed, is_renting, is_returning, last_reported,num_bikes_available,num_docks_available,date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (_station_id, _station_is_installed, _station_is_renting, _station_is_returning, _station_last_reported, _station_num_bikes_available, _station_num_docks_available,dt_object))
        conn.commit()
        print('Data at {} added to POSTGRESQL'.format(dt_object))
    conn.close()

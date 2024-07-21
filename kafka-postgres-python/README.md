
https://ffaheroes.medium.com/end-to-end-distributed-queue-with-kafka-postgresql-and-python-2424d58fdcbb
## We will build an end to end data pipeline that will allow us to monitor live data about the Oslo City Bike.
## The goal is to see available docks & bikes in real time, change in status and represent them in map.

# python environment sst
```
$ python -m venv .venv
$ source .venv/Scripts/activate
$ pip install -r requirements.txt

$ cat requirements.txt
kafka-python

$  python -m pip freeze
kafka-python==2.0.2
psycopg2==2.9.9
```

# Kafka topic
```
$ docker exec -it  kafka-docker-kafka-1 kafka-topics.sh  --bootstrap-server localhost:9092 --list
__consumer_offsets
solobyte-kafka-primer-topic
test

$ docker exec -it  kafka-docker-kafka-1 kafka-topics.sh  --bootstrap-server localhost:9092 --describe --topic test
Topic: test     TopicId: H8nHQVwmQyCYYJ9HCgAJkg PartitionCount: 1       ReplicationFactor: 1    Configs:
        Topic: test     Partition: 0    Leader: 0       Replicas: 0     Isr: 0



$ docker exec -it  kafka-docker-kafka-1  kafka-console-consumer.sh  --bootstrap-server localhost:9092 --topic test --from-beginning
Processed a total of 6 messages

kafka-console-consumer.sh --formatter "kafka.coordinator.group.GroupMetadataManager\$OffsetsMessageFormatter" --bootstrap-server localhost:9092 --topic test --from-beginning

kafka-consumer-groups.sh --bootstrap-server localhost:9092 --group my-group --describe
i
 kafka-topics.sh  --bootstrap-server localhost:9092 --delete --topic test

kafka-run-class.sh kafka.tools.GetOffsetShell --broker-list localhost:9092 --topic test --time -2

kafka-consumer-groups.sh --bootstrap-server localhost:9092 --list
console-consumer-53658
my-group
console-consumer-21749
test-group-id
```
# Database and table
```
docker exec -it  postgres-docker-postgres-1 psql -U root -c"create database oslo_city_bike" -c "\dn;"

Madhavi@madhavikrishna MINGW64 /d/Sanjeev/Learn/python/practice-python/kafka-postgres-python (main)
$ docker exec -it  postgres-docker-postgres-1 psql -U root oslo_city_bike -c'\l'
                                     List of databases
      Name      |   Owner   | Encoding |  Collate   |   Ctype    |    Access privileges
----------------+-----------+----------+------------+------------+-------------------------
 org_db         | root      | UTF8     | en_US.utf8 | en_US.utf8 |
 oslo_city_bike | root      | UTF8     | en_US.utf8 | en_US.utf8 |
 postgres       | root      | UTF8     | en_US.utf8 | en_US.utf8 |
 root           | root      | UTF8     | en_US.utf8 | en_US.utf8 |
 template0      | root      | UTF8     | en_US.utf8 | en_US.utf8 | =c/root                +
                |           |          |            |            | root=CTc/root
 template1      | root      | UTF8     | en_US.utf8 | en_US.utf8 | =c/root                +
                |           |          |            |            | root=CTc/root
 testdb         | test_user | UTF8     | en_US.utf8 | en_US.utf8 | =Tc/test_user          +
                |           |          |            |            | test_user=CTc/test_user
 wiki           | root      | UTF8     | en_US.utf8 | en_US.utf8 |
(8 rows)


What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug postgres-docker-postgres-1
    Learn more at https://docs.docker.com/go/debug-cli/
(.venv)
Madhavi@madhavikrishna MINGW64 /d/Sanjeev/Learn/python/practice-python/kafka-postgres-python (main)
$ docker exec -it  postgres-docker-postgres-1 psql -U root oslo_city_bike -c'\dt'
            List of relations
 Schema |      Name      | Type  | Owner
--------+----------------+-------+-------
 public | station_status | table | root
(1 row)


What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug postgres-docker-postgres-1
    Learn more at https://docs.docker.com/go/debug-cli/
(.venv)
Madhavi@madhavikrishna MINGW64 /d/Sanjeev/Learn/python/practice-python/kafka-postgres-python (main)
$ docker exec -it  postgres-docker-postgres-1 psql -U root oslo_city_bike -c'\d+ station_status'
                                                     Table "public.station_status"
       Column        |           Type           | Collation | Nullable | Default | Storage  | Compression | Stats target | Description
---------------------+--------------------------+-----------+----------+---------+----------+-------------+--------------+-------------
 station_id          | character(20)            |           | not null |         | extended |             |
 |
 is_installed        | character(20)            |           | not null |         | extended |             |
 |
 is_renting          | integer                  |           |          |         | plain    |             |
 |
 is_returning        | integer                  |           |          |         | plain    |             |
 |
 last_reported       | integer                  |           |          |         | plain    |             |
 |
 num_bikes_available | integer                  |           |          |         | plain    |             |
 |
 num_docks_available | integer                  |           |          |         | plain    |             |
 |
 created_at          | timestamp with time zone |           | not null | now()   | plain    |             |
 |
 updated_at          | timestamp with time zone |           | not null | now()   | plain    |             |
 |
Triggers:
    set_updated_at BEFORE UPDATE ON station_status FOR EACH ROW EXECUTE FUNCTION trigger_set_updated_at_timestamp()
Access method: heap


What's next:
    Try Docker Debug for seamless, persistent debugging tools in any container or image → docker debug postgres-docker-postgres-1
    Learn more at https://docs.docker.com/go/debug-cli/
(.venv)
```

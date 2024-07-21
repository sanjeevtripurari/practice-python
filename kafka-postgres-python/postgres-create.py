import psycopg2

conn = psycopg2.connect(database = "oslo_city_bike", user='root', password='secret', host='127.0.0.1', port='5432')
cursor = conn.cursor()

#Creating Database 'Oslo_city_bike'

# sql = '''CREATE DATABASE IF NOT EXISTS Oslo_city_bike''';
# cursor.execute(sql)
# conn.commit()

# Creating Table Station_Status

sql='''
              -- Create Table Station_status

              CREATE TABLE IF NOT EXISTS Station_status (
              Station_id           char(20)    NOT NULL,
              is_installed         char(20)    NOT NULL,
              is_renting           int,
              is_returning         int,
              last_reported        int,
              num_bikes_available  int,
              num_docks_available  int,
              created_at           timestamptz NOT NULL DEFAULT now(),
              updated_at           timestamptz NOT NULL DEFAULT now());

              -- Create Function for record update in Station_status

              CREATE OR REPLACE FUNCTION trigger_set_updated_at_timestamp()
              RETURNS TRIGGER AS $$

              BEGIN
                NEW.updated_at = NOW();
                RETURN NEW;
              END;
              $$ LANGUAGE plpgsql;

              -- Create Trigger for record update in Station_status
              CREATE TRIGGER set_updated_at
                    BEFORE UPDATE ON Station_status 
                    FOR EACH ROW
                    EXECUTE PROCEDURE trigger_set_updated_at_timestamp();

              '''

cursor.execute(sql)
conn.commit()
conn.close()


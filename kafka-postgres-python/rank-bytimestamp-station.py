WITH
T1 as 
(select
     station_id,
     num_bikes_available,
     num_docks_available,
     date,
     last_reported,
     LAG(last_reported,1) over (partition by station_id order by    last_reported) as prevtime,
     LAG(date,1) over (partition by station_id order by  last_reported) as prevdate
from
 station_status)


select
 station_information.name,
 t1.station_id,
 right(t1.date,9) as date,
 t1.num_bikes_available,
 t1.num_docks_available,
 t1.prevdate,
 T2.num_bikes_available,
 t1.num_bikes_available-T2.num_bikes_available as Change,
 concat(station_information.lat,',',station_information.lon) as Coordinate
from
 t1
inner join
    (select * from station_status) as T2
 ON
    T1.station_id = T2.station_id
 AND
    T1.prevtime = T2.last_reported
inner join
 station_information
 ON
 T1.station_id = station_information.station_id
where (t1.num_bikes_available-T2.num_bikes_available) <>0
order by
 t1.date desc

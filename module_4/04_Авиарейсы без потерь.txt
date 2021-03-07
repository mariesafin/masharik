SELECT a.city,
       count(a.airport_code)
FROM dst_project.airports a
GROUP BY city
HAVING count(a.airport_code)>1

SELECT count(DISTINCT status)
FROM dst_project.flights

SELECT DISTINCT status
FROM dst_project.flights

SELECT count(status)
FROM dst_project.flights
WHERE status='Departed'

SELECT *
FROM dst_project.aircrafts -- код боинга 777 - 773

SELECT count(DISTINCT seat_no)
FROM dst_project.seats
WHERE aircraft_code='773'
  
SELECT count(flight_id)
FROM dst_project.flights 
WHERE (actual_arrival BETWEEN '2017-04-01' AND '2017-09-01')
  AND (status = 'Arrived')
  
SELECT count(flight_id)
FROM dst_project.flights
WHERE status = 'Cancelled'
    
SELECT *
FROM dst_project.aircrafts
WHERE model like 'Boeing%'

SELECT *
FROM dst_project.aircrafts
WHERE model like 'Sukhoi Superjet%'

SELECT *
FROM dst_project.aircrafts
WHERE model like 'Airbus%'

SELECT count(*)
FROM dst_project.airports
WHERE timezone like 'Europe%'

SELECT count(*)
FROM dst_project.airports
WHERE timezone like 'Asia%'

SELECT count(*)
FROM dst_project.airports
WHERE timezone like 'Australia%'

SELECT *
FROM dst_project.flights
WHERE actual_departure IS NOT NULL

SELECT flight_id,
       scheduled_arrival,
       actual_arrival,
       actual_arrival-scheduled_arrival
FROM dst_project.flights
WHERE actual_arrival IS NOT NULL
ORDER BY actual_arrival-scheduled_arrival DESC

SELECT *
FROM dst_project.flights
ORDER BY scheduled_departure

SELECT *,
       scheduled_arrival-scheduled_departure 
	   /*flight_id,
       scheduled_departure,
       scheduled_arrival,
       scheduled_arrival-scheduled_departure*/
FROM dst_project.flights --where actual_arrival is not null
ORDER BY scheduled_arrival-scheduled_departure DESC

SELECT avg(DATE_PART('hour', scheduled_arrival - scheduled_departure) * 60 + DATE_PART('minute', scheduled_arrival - scheduled_departure)) AS avg_flight_duration
FROM dst_project.flights
WHERE scheduled_departure IS NOT NULL

SELECT fare_conditions,
       count(*)
FROM dst_project.seats
WHERE aircraft_code='SU9'
GROUP BY fare_conditions
ORDER BY 2 DESC

SELECT *
FROM dst_project.bookings
ORDER BY total_amount

SELECT *
FROM dst_project.tickets t
JOIN dst_project.boarding_passes b ON t.ticket_no=b.ticket_no
WHERE t.passenger_id='4313 788533'

SELECT *
FROM dst_project.airports
WHERE city='Anapa' --код Анапы AAQ

SELECT count(*)
FROM dst_project.flights
WHERE arrival_airport='AAQ'
  AND status='Arrived'
  AND DATE_PART('year', actual_arrival)=2017
    
SELECT count(*)
FROM dst_project.flights
WHERE departure_airport='AAQ' 
  --AND status='Arrived'
  AND DATE_PART('year', actual_departure)=2017
  AND DATE_PART('month', actual_departure) in (1,2,12)
    
SELECT *
FROM dst_project.flights
WHERE departure_airport='AAQ'
  AND status='Cancelled' 
    
SELECT *
FROM dst_project.airports
WHERE city='Moscow' --SVO,VKO,DME

SELECT count(*) --count(distinct flight_no)
FROM dst_project.flights
WHERE departure_airport='AAQ'
  AND arrival_airport NOT IN ('SVO','VKO','DME')

SELECT a.model,
       count(DISTINCT s.seat_no)
FROM dst_project.aircrafts a
JOIN dst_project.seats s ON a.aircraft_code=s.aircraft_code
JOIN dst_project.flights f ON f.aircraft_code=s.aircraft_code
WHERE departure_airport='AAQ'
GROUP BY a.model
ORDER BY 2 DESC




--ПЕРЕХОДИМ К РЕАЛЬНОЙ АНАЛИТИКЕ

/*SELECT flight_id,
       SUM(amount) flight_amount
FROM dst_project.ticket_flights
GROUP BY flight_id

select * from dst_project.airports

select 
    aircraft_code, 
    count(seat_no) seat_count
from dst_project.seats
group by aircraft_code 

select asin(sin(pi()))*/



--ОСНОВНОЙ КОД ДЛЯ ПОЛУЧЕНИЯ НУЖНОГО ДАТАСЕТА:



SELECT f.*,
f.actual_arrival - f.actual_departure flight_duration,

a1.city departure_city,
a1.latitude departure_latitude,
a1.longitude departure_longitude,

a2.city arrival_city,
a2.latitude arrival_latitude,
a2.longitude arrival_longitude,

2 * 6371 * asin(
    sqrt(sin((a1.latitude-a2.latitude)*PI()/360.0) * sin((a1.latitude-a2.latitude)*PI()/360.0)
        + sin((a1.longitude-a2.longitude)*PI()/360.0) * sin((a1.longitude-a2.longitude)*PI()/360.0) * cos(a1.latitude*PI()/180.0) * cos(a2.latitude*PI()/180.0))) distance,
		--нахождение расстояния между городами рейса

ac.model,
ac.range,
s.seat_count,

tf.flight_amount,
tf.ticket_count

FROM dst_project.flights f
JOIN dst_project.airports a1 ON f.departure_airport=a1.airport_code
JOIN dst_project.airports a2 ON f.arrival_airport=a2.airport_code
JOIN dst_project.aircrafts ac ON f.aircraft_code=ac.aircraft_code
JOIN (SELECT flight_id,
            count(*) ticket_count, --находим количество проданных билетов
            SUM(amount) flight_amount --находим сумму выручки проданных билетов на рейс
        FROM
            dst_project.ticket_flights
        group by flight_id) tf on f.flight_id = tf.flight_id
JOIN (select aircraft_code, 
            count(seat_no) seat_count
        from dst_project.seats
        group by aircraft_code ) s on f.aircraft_code = s.aircraft_code
WHERE f.departure_airport = 'AAQ'
  AND (date_trunc('month', f.scheduled_departure) in ('2017-01-01','2017-02-01', '2017-12-01'))
  AND f.status not in ('Cancelled')
  
 

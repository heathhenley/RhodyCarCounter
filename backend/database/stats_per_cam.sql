select c.name , avg(d. vehicles), stddev(d.vehicles)
  from vehicle_frequency_data as d, camera as c
  where d.camera_id = c.id  group by c.name 

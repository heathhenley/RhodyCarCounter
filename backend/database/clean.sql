delete from vehicle_frequency_data where timestamp - now() > (interval '1 week')

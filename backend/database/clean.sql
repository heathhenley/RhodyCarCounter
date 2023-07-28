delete from vehicle_frequency_data where now() - timestamp > (interval '6 weeks')

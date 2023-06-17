INSERT INTO transport_infrastructure(water_transport, underground_transport, ground_transport,
                                     transport_rent, transfer, public_transport,
                                     rented_transport, taxi, cost, ti_value)  VALUES
(True, True, True, True, 0.34, 0.45, 0.11, 0.22, 0.33, 1.54),
(True, False, True, True, 0.30, 0.44, 0.12, 0.24, 0.38, 1.52),
(True, True, False, True, 0.33, 0.43, 0.13, 0.25, 0.37, 1.54),
(True, True, False, False, 0.32, 0.42, 0.14, 0.26, 0.36, 1.55),
(True, True, True, False, 0.31, 0.41, 0.15, 0.27, 0.35, 1.56);

INSERT INTO food_segment(products, local_eating_places, type_of_place, cost, variety, national_features, fs_value) VALUES
(0.8, 0.7, 0.2, 0.5, 0.5, True, 1.5),
(0.7, 0.4, 0.3,0.6, 0.4, False, 2.5),
(0.6, 0.3, 0.4,0.7, 0.3, True, 2.5),
(0.5, 0.1, 0.5,0.8, 0.2, False, 3.5),
(0.4, 0.2, 0.6,0.9, 0.1, False, 4.1);

INSERT INTO num_factors(hotels, hostels, restaurants, malls, hospitals, resorts, food_price) VALUES
(1000, 2000, 3000, 40000, 2000, 1000, 123.10),
(2000, 5000, 2000, 60000, 1000, 2000, 523.10),
(3000, 4000, 1000, 50000, 3000, 3000, 423.10),
(4000, 3000, 5000, 10000, 4000, 4000, 323.10),
(5000, 1000, 6000, 20000, 5000, 5000, 223.10);

INSERT INTO other_factors(visa_fees, popular_resort, natural_factors, number_tourists, of_value) VALUES
(True, 0.5, 0.6, 0.1, 1.2),
(False, 0.4, 0.1,0.2, 1.3),
(True, 0.3, 0.3, 0.3,1.4),
(True, 0.2, 0.2, 0.4,1.5),
(False, 0.1, 0.4, 0.5,1.6);

INSERT INTO segment_accommodation(type_of_housing, consumer_infr, house, apartment,
                                  hotel, hostel, camping, green_territory, medical_institutions,
                                  shopping_malls, neighbourhood, cost, as_value) VALUES
(0.3, 0.2, False, True, False, False, True, True, False, True, 0.1, 0.32, 4.2),
(0.2, 0.6, True, True, True, True, False, True, True, True, 0.2, 0.33, 4.6),
(0.4, 0.5, True, False, True, True, False, False, False, False, 0.3, 0.34, 4.5),
(0.5, 0.4, False, False, True, True, True, False, True, True, 0.4, 0.35, 4.4),
(0.6, 0.1, False, True, False, False, False, True, True, False, 0.5, 0.36, 4.3);

INSERT INTO leisure_and_recreation(historical_landscaping, natural_features,
                                   events, wellness_holiday, shopping,
                                   unique_objects, unique_zones, lr_value) VALUES
(0.3, 0.5, True, 0.6, 0.4, True, False, 3.22),
(0.2, 0.5, False, 0.2, 0.5, False, True, 3.23),
(0.1, 0.4, True, 0.1, 0.4, True, True, 3.24),
(0.4, 0.3, False, 0.4, 0.3, False, True, 3.25),
(0.5, 0.2, True, 0.5, 0.2, True, False, 3.26);

INSERT INTO area(area_type, name) VALUES
('Страна', 'Россия'),
('Город', 'Москва'),
('Город', 'Санкт-Питербур'),
('Город', 'Курск');

INSERT INTO factors(area_id, date, ti_id, sa_id, fs_id, lr_id, of_id, nf_id, tourist_flow) VALUES
(1, '2017', 1, 2, 3, 4, 5, 1, 1000000),
(1, '2016', 2, 1, 3, 2, 2, 2, 1200000),
(1, '2015', 1, 2, 5, 3, 1, 3, 1300000),
(1, '2014', 5, 3, 4, 1, 2, 4, 1400000),
(1, '2013', 4, 4, 3, 2, 3, 5, 1500000),
(1, '2012', 3, 5, 2, 5, 2, 1, 1600000),
(1, '2011', 2, 2, 1, 1, 4, 2, 1700000),
(1, '01-01-2016', 1, 2, 3, 4, 5, 2, 1000000),
(1, '02-2015', 5, 5, 1, 5, 3, 2, 1000000),
(2, '2017', 4, 5, 2, 4, 3, 3, 1000000),
(3, '2017', 2, 3, 4, 5, 1, 2, 1000000);

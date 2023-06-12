CREATE TABLE IF NOT EXISTS transport_infrastructure (
  id serial,
  water_transport boolean,
  underground_transport boolean,
  ground_transport boolean,
  transport_rent boolean,
  transfer decimal,
  public_transport decimal,
  rented_transport decimal,
  taxi decimal,
  cost decimal,
  ti_value decimal NOT NULL,
  CONSTRAINT pk_transport_infrastructure PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS food_segment (
  id serial,
  products decimal,
  local_eating_places decimal,
  cost decimal,
  variety decimal,
  national_features boolean,
  fs_value decimal NOT NULL ,
  CONSTRAINT pk_food_segment PRIMARY KEY (id)
);


CREATE TABLE other_factors (
  id serial,
  visa_fees boolean,
  popular_resort decimal,
  natural_factors decimal,
  of_value decimal NOT NULL ,
  CONSTRAINT pk_other_factors PRIMARY KEY (id)
);


CREATE TABLE accommodation_segment (
  id serial,
  type_of_housing decimal,
  consumer_infr decimal,
  house boolean,
  apartment boolean,
  hotel boolean,
  hostel boolean,
  camping boolean,
  green_territory boolean,
  medical_institutions boolean,
  shopping_malls boolean,
  cost decimal,
  as_value decimal NOT NULL,
  CONSTRAINT pk_accommodation_segment PRIMARY KEY (id)
);


CREATE TABLE leisure_and_recreation (
  id serial,
  historical_landscaping decimal,
  natural_features decimal,
  events boolean,
  wellness_holiday decimal,
  shopping decimal,
  unique_objects boolean,
  unique_zones boolean,
  lr_value decimal NOT NULL,
  CONSTRAINT pk_leisure_and_recreation PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS gost (
  id serial,
  ti_id integer NOT NULL,
  as_id integer NOT NULL,
  fs_id integer NOT NULL,
  lr_id integer NOT NULL,
  of_id integer NOT NULL,
  CONSTRAINT pk_gost PRIMARY KEY (id),
  CONSTRAINT fk_gost_ti
    FOREIGN KEY (ti_id)
      REFERENCES transport_infrastructure("id"),
  CONSTRAINT fk_gost_fs
    FOREIGN KEY (fs_id)
      REFERENCES food_segment(id),
  CONSTRAINT fk_gost_of
    FOREIGN KEY (of_id)
      REFERENCES other_factors(id),
  CONSTRAINT fk_gost_as
    FOREIGN KEY (as_id)
      REFERENCES accommodation_segment(id),
  CONSTRAINT fk_gost_lr
    FOREIGN KEY (lr_id)
      REFERENCES leisure_and_recreation(id)
);


CREATE TABLE IF NOT EXISTS tourism_type (
  id serial,
  name text NOT NULL,
  id_gost integer NOT NULL,
  CONSTRAINT pk_tourism_type PRIMARY KEY (id),
  CONSTRAINT fk_tourism_type_gost
    FOREIGN KEY (id_gost)
      REFERENCES gost(id)
);

CREATE TABLE IF NOT EXISTS area (
  id serial,
  area_type text NOT NULL ,
  name text NOT NULL ,
  CONSTRAINT pk_area PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS factors_set (
  id serial,
  area_id integer NOT NULL,
  date date NOT NULL,
  ti_id integer NOT NULL,
  as_id integer NOT NULL,
  fs_id integer NOT NULL,
  lr_id integer NOT NULL,
  of_id integer NOT NULL,
  tourist_flow decimal NOT NULL,
  CONSTRAINT pk_factors_set PRIMARY KEY (id),
  CONSTRAINT fk_factors_set_ti
    FOREIGN KEY (ti_id)
      REFERENCES transport_infrastructure("id"),
  CONSTRAINT fk_factors_set_fs
    FOREIGN KEY (fs_id)
      REFERENCES food_segment(id),
  CONSTRAINT fk_factors_set_of
    FOREIGN KEY (of_id)
      REFERENCES other_factors(id),
  CONSTRAINT fk_factors_set_as
    FOREIGN KEY (as_id)
      REFERENCES accommodation_segment(id),
  CONSTRAINT fk_factors_set_lr
    FOREIGN KEY (lr_id)
      REFERENCES leisure_and_recreation(id),
  CONSTRAINT fk_factors_set_lr_area
    FOREIGN KEY (area_id)
      REFERENCES area(id)
);


CREATE TABLE IF NOT EXISTS route (
  id serial,
  id_from integer NOT NULL,
  id_to integer NOT NULL,
  date date NOT NULL,
  tourists integer NOT NULL,
  CONSTRAINT pk_route PRIMARY KEY (id),
  CONSTRAINT fk_route_from
    FOREIGN KEY (id_from)
      REFERENCES area(id),
  CONSTRAINT fk_route_to
    FOREIGN KEY (id_to)
      REFERENCES area(id)
);

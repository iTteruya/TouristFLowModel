CREATE TABLE IF NOT EXISTS num_factors (
  id serial,
  hotels integer,
  hostels integer,
  restaurants integer,
  malls integer,
  hospitals integer,
  resorts integer,
  food_price decimal,
  CONSTRAINT pk_num_factors PRIMARY KEY (id)
);

-- Create the transport_infrastructure table
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

-- Create the trigger function to calculate ti_value
CREATE OR REPLACE FUNCTION calculate_ti_value()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.ti_value := COALESCE(NEW.transfer, 0) + COALESCE(NEW.public_transport, 0) +
                  COALESCE(NEW.rented_transport, 0) + COALESCE(NEW.taxi, 0) +
                  COALESCE(NEW.cost, 0);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to automatically update ti_value
CREATE TRIGGER update_ti_value_trigger
  BEFORE INSERT OR UPDATE ON transport_infrastructure
  FOR EACH ROW
  EXECUTE FUNCTION calculate_ti_value();


-- Create the food_segment table
CREATE TABLE IF NOT EXISTS food_segment (
  id serial,
  products decimal,
  local_eating_places decimal,
  type_of_place decimal,
  cost decimal,
  variety decimal,
  national_features boolean,
  fs_value decimal NOT NULL,
  CONSTRAINT pk_food_segment PRIMARY KEY (id)
);

-- Create the trigger function to calculate fs_value
CREATE OR REPLACE FUNCTION calculate_fs_value()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.fs_value := COALESCE(NEW.products, 0) + COALESCE(NEW.local_eating_places, 0) +
                  COALESCE(NEW.cost, 0) + COALESCE(NEW.variety, 0) + COALESCE(NEW.type_of_place, 0) +
                  CASE WHEN NEW.national_features THEN 1 ELSE 0 END;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to automatically update fs_value
CREATE TRIGGER update_fs_value_trigger
  BEFORE INSERT OR UPDATE ON food_segment
  FOR EACH ROW
  EXECUTE FUNCTION calculate_fs_value();


-- Create the other_factors table
CREATE TABLE IF NOT EXISTS other_factors (
  id serial,
  visa_fees boolean,
  popular_resort decimal,
  natural_factors decimal,
  number_tourists decimal,
  of_value decimal NOT NULL,
  CONSTRAINT pk_other_factors PRIMARY KEY (id)
);

-- Create the trigger function to calculate of_value
CREATE OR REPLACE FUNCTION calculate_of_value()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.of_value := COALESCE(NEW.popular_resort, 0) + COALESCE(NEW.natural_factors, 0) +
                  COALESCE(NEW.number_tourists, 0) +
                  CASE WHEN NEW.visa_fees THEN 1 ELSE 0 END;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to automatically update of_value
CREATE TRIGGER update_of_value_trigger
  BEFORE INSERT OR UPDATE ON other_factors
  FOR EACH ROW
  EXECUTE FUNCTION calculate_of_value();


-- Create the segment_accommodation table
CREATE TABLE IF NOT EXISTS segment_accommodation (
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
  neighbourhood decimal,
  cost decimal,
  as_value decimal NOT NULL,
  CONSTRAINT pk_segment_accommodation PRIMARY KEY (id)
);

-- Create the trigger function to calculate as_value
CREATE OR REPLACE FUNCTION calculate_as_value()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.as_value := COALESCE(NEW.type_of_housing, 0) + COALESCE(NEW.consumer_infr, 0) + + COALESCE(NEW.neighbourhood, 0) +
                  CASE WHEN NEW.house THEN 1 ELSE 0 END +
                  CASE WHEN NEW.apartment THEN 1 ELSE 0 END +
                  CASE WHEN NEW.hotel THEN 1 ELSE 0 END +
                  CASE WHEN NEW.hostel THEN 1 ELSE 0 END +
                  CASE WHEN NEW.camping THEN 1 ELSE 0 END +
                  CASE WHEN NEW.green_territory THEN 1 ELSE 0 END +
                  CASE WHEN NEW.medical_institutions THEN 1 ELSE 0 END +
                  CASE WHEN NEW.shopping_malls THEN 1 ELSE 0 END +
                  COALESCE(NEW.cost, 0);
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to automatically update as_value
CREATE TRIGGER update_as_value_trigger
  BEFORE INSERT OR UPDATE ON segment_accommodation
  FOR EACH ROW
  EXECUTE FUNCTION calculate_as_value();


-- Create the leisure_and_recreation table
CREATE TABLE IF NOT EXISTS leisure_and_recreation (
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

-- Create the trigger function to calculate lr_value
CREATE OR REPLACE FUNCTION calculate_lr_value()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.lr_value := COALESCE(NEW.historical_landscaping, 0) + COALESCE(NEW.natural_features, 0) +
                  COALESCE(NEW.wellness_holiday, 0) + COALESCE(NEW.shopping, 0) +
                  CASE WHEN NEW.events THEN 1 ELSE 0 END +
                  CASE WHEN NEW.unique_objects THEN 1 ELSE 0 END +
                  CASE WHEN NEW.unique_zones THEN 1 ELSE 0 END;
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Create the trigger to automatically update lr_value
CREATE TRIGGER update_lr_value_trigger
  BEFORE INSERT OR UPDATE ON leisure_and_recreation
  FOR EACH ROW
  EXECUTE FUNCTION calculate_lr_value();



CREATE TABLE IF NOT EXISTS gost (
  id serial,
  ti_id integer NOT NULL,
  sa_id integer NOT NULL,
  fs_id integer NOT NULL,
  lr_id integer NOT NULL,
  of_id integer NOT NULL,
  nf_id integer NOT NULL,
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
    FOREIGN KEY (sa_id)
      REFERENCES segment_accommodation (id),
  CONSTRAINT fk_gost_lr
    FOREIGN KEY (lr_id)
      REFERENCES leisure_and_recreation(id),
  CONSTRAINT fk_factors_ng
    FOREIGN KEY (nf_id)
      REFERENCES num_factors(id)
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


CREATE TABLE IF NOT EXISTS factors (
  id serial,
  area_id integer NOT NULL,
  date text NOT NULL,
  ti_id integer NOT NULL,
  sa_id integer NOT NULL,
  fs_id integer NOT NULL,
  lr_id integer NOT NULL,
  of_id integer NOT NULL,
  nf_id integer NOT NULL,
  tourist_flow decimal NOT NULL,
  CONSTRAINT pk_factors PRIMARY KEY (id),
  CONSTRAINT fk_factors_ti
    FOREIGN KEY (ti_id)
      REFERENCES transport_infrastructure("id"),
  CONSTRAINT fk_factors_fs
    FOREIGN KEY (fs_id)
      REFERENCES food_segment(id),
  CONSTRAINT fk_factors_of
    FOREIGN KEY (of_id)
      REFERENCES other_factors(id),
  CONSTRAINT fk_factors_sa
    FOREIGN KEY (sa_id)
      REFERENCES segment_accommodation (id),
  CONSTRAINT fk_factors_lr
    FOREIGN KEY (lr_id)
      REFERENCES leisure_and_recreation(id),
  CONSTRAINT fk_factors_area
    FOREIGN KEY (area_id)
      REFERENCES area(id),
  CONSTRAINT fk_factors_ng
    FOREIGN KEY (nf_id)
      REFERENCES num_factors(id)
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

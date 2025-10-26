create table public.weather_data (
  farm_id text not null,
  date date not null,
  wind_direction text null,
  weather_code integer null,
  temperature_high numeric(5, 2) null,
  temperature_low numeric(5, 2) null,
  temperature_mean numeric(5, 2) null,
  precipitation_chance numeric(5, 2) null,
  precipitation_sum numeric(8, 4) null,
  wind_speed_max numeric(6, 2) null,
  wind_gusts_max numeric(6, 2) null,
  humidity_mean numeric(5, 2) null,
  evapotranspiration numeric(8, 4) null,
  sunshine_duration numeric(10, 2) null,
  dew_point numeric(5, 2) null,
  constraint weather_data_pkey primary key (farm_id, date)
) TABLESPACE pg_default;
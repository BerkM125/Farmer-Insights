create table public.environmental_data (
  farm_id text not null,
  date text null,
  soil_ph double precision null,
  soil_temperature_c double precision null,
  sediment_level_mg_l double precision null,
  erosion_risk_index double precision null,
  fertilizer_availability_index double precision null,
  broad_advice text null,
  task_recommendations text[] null,
  ph_url text null,
  nitrogen_levels double precision[] null,
  constraint environmental_data_pkey primary key (farm_id)
) TABLESPACE pg_default;
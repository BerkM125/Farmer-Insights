create table public.market_prices (
  id serial not null,
  date character varying(7) not null,
  crop_name character varying(100) not null,
  unit character varying(50) not null,
  price numeric(10, 2) not null,
  constraint market_prices_pkey primary key (id),
  constraint market_prices_date_crop_name_key unique (date, crop_name)
) TABLESPACE pg_default;

create index IF not exists idx_market_prices_crop_date on public.market_prices using btree (crop_name, date desc) TABLESPACE pg_default;
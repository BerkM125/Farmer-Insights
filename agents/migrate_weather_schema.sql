-- Migration script to update weather_data table schema
-- This adds all the new weather fields from the updated DailyWeather model

-- Add new columns to weather_data table
ALTER TABLE weather_data 
ADD COLUMN IF NOT EXISTS weather_code INTEGER,
ADD COLUMN IF NOT EXISTS temperature_high DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS temperature_low DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS temperature_mean DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS precipitation_chance DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS precipitation_sum DECIMAL(8,4),
ADD COLUMN IF NOT EXISTS wind_speed_max DECIMAL(6,2),
ADD COLUMN IF NOT EXISTS wind_gusts_max DECIMAL(6,2),
ADD COLUMN IF NOT EXISTS humidity_mean DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS evapotranspiration DECIMAL(8,4),
ADD COLUMN IF NOT EXISTS sunshine_duration DECIMAL(10,2),
ADD COLUMN IF NOT EXISTS dew_point DECIMAL(5,2),
ADD COLUMN IF NOT EXISTS growing_degree_days DECIMAL(8,2),
ADD COLUMN IF NOT EXISTS leaf_wetness_probability DECIMAL(5,2);

-- Update existing columns to match new naming convention
-- Note: These ALTER COLUMN statements may need to be adjusted based on your current schema
-- If columns already exist with different names, you may need to rename them instead

Optional: Drop old columns if they exist and are no longer needed
ALTER TABLE weather_data DROP COLUMN IF EXISTS temperature_high_f;
ALTER TABLE weather_data DROP COLUMN IF EXISTS temperature_low_f;
ALTER TABLE weather_data DROP COLUMN IF EXISTS rainfall_chance;
ALTER TABLE weather_data DROP COLUMN IF EXISTS rainfall_amount_mm;
ALTER TABLE weather_data DROP COLUMN IF EXISTS humidity_percent;
ALTER TABLE weather_data DROP COLUMN IF EXISTS wind_speed_mph;
ALTER TABLE weather_data DROP COLUMN IF EXISTS condition;

-- Add indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_weather_data_farm_date ON weather_data(farm_id, date);
CREATE INDEX IF NOT EXISTS idx_weather_data_date ON weather_data(date);

-- Add comments to document the new schema
COMMENT ON COLUMN weather_data.weather_code IS 'WMO weather code (0-99)';
COMMENT ON COLUMN weather_data.temperature_high IS 'High temperature in Fahrenheit';
COMMENT ON COLUMN weather_data.temperature_low IS 'Low temperature in Fahrenheit';
COMMENT ON COLUMN weather_data.temperature_mean IS 'Mean temperature in Fahrenheit';
COMMENT ON COLUMN weather_data.precipitation_chance IS 'Chance of precipitation (0-100)';
COMMENT ON COLUMN weather_data.precipitation_sum IS 'Total precipitation amount in inches';
COMMENT ON COLUMN weather_data.wind_speed_max IS 'Maximum wind speed in mph';
COMMENT ON COLUMN weather_data.wind_gusts_max IS 'Maximum wind gusts in mph';
COMMENT ON COLUMN weather_data.humidity_mean IS 'Mean relative humidity percentage';
COMMENT ON COLUMN weather_data.evapotranspiration IS 'Evapotranspiration in inches';
COMMENT ON COLUMN weather_data.sunshine_duration IS 'Sunshine duration in seconds';
COMMENT ON COLUMN weather_data.dew_point IS 'Dew point temperature in Fahrenheit';
COMMENT ON COLUMN weather_data.growing_degree_days IS 'Growing degree days';
COMMENT ON COLUMN weather_data.leaf_wetness_probability IS 'Leaf wetness probability';

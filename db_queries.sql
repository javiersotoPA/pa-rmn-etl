-- Crear la tabla para 'Desk study'
CREATE TABLE pa_restoration_monitoring_network.desk_study (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    site VARCHAR,
    condition_category VARCHAR,
    visit VARCHAR,
    aerial_imagery_notes VARCHAR,
    land_use VARCHAR,
    land_use_notes VARCHAR,
    land_use_change_notes VARCHAR,
    desk_deer_density_notes VARCHAR,
    desk_herbivore_impact_notes VARCHAR,
    desk_general_notes VARCHAR
);

-- Crear la tabla para 'Quadrat information'
CREATE TABLE pa_restoration_monitoring_network.quadrat_information (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    sampling_point VARCHAR,
    date DATE,
    surveyors VARCHAR,
    markers_found VARCHAR,
    feature_type VARCHAR,
    quadrat_type VARCHAR,
    aspect VARCHAR,
    peat_depth INTEGER,
    bare_peat DECIMAL,
    bare_mineral DECIMAL,
    open_water DECIMAL,
    litter DECIMAL,
    trampling VARCHAR,
    dung VARCHAR,
    trees VARCHAR,
    veg_height_1 INTEGER,
    veg_height_2 INTEGER,
    veg_height_3 INTEGER,
    veg_height_4 INTEGER,
    veg_height_5 INTEGER,
    disturbance_notes VARCHAR,
    quadrat_notes VARCHAR
);

-- Crear la tabla para 'Vegetation'
CREATE TABLE pa_restoration_monitoring_network.vegetation (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    species VARCHAR,
    cover DECIMAL
);

-- Crear la tabla para 'Feature status - drains'
CREATE TABLE pa_restoration_monitoring_network.feature_status_drains (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    drain_point VARCHAR,
    drain_identifiable BOOLEAN,
    drain_depth VARCHAR,
    drain_width VARCHAR,
    drain_flow VARCHAR,
    drain_bare_peat VARCHAR,
    drain_bare_mineral VARCHAR,
    drain_open_water VARCHAR,
    drain_litter VARCHAR,
    drain_vegetation VARCHAR,
    drain_dwarf_shrub VARCHAR,
    drain_eriophorum VARCHAR,
    drain_trichophorum VARCHAR,
    drain_molinia VARCHAR,
    drain_other_poaceae VARCHAR,
    drain_juncus VARCHAR,
    drain_sphagnum VARCHAR,
    drain_other_moss VARCHAR,
    drain_lichen VARCHAR,
    drain_block VARCHAR,
    drain_block_erosion_around VARCHAR,
    drain_block_erosion_over VARCHAR,
    drain_block_trampling VARCHAR,
    drain_block_water VARCHAR,
    drain_block_water_sphagnum VARCHAR,
    drain_block_sediment VARCHAR,
    drain_block_vegetation VARCHAR,
    drain_donor BOOLEAN,
    drain_donor_vegetation VARCHAR,
    drain_score VARCHAR,
    drain_notes VARCHAR
);

-- Crear la tabla para 'Photos'
CREATE TABLE pa_restoration_monitoring_network.photos (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    title VARCHAR,
    date DATE,
    photographer VARCHAR,
    bearing INTEGER,
    photo_notes VARCHAR,
    dams_link VARCHAR
);

-- Crear la tabla para 'monitoring_area'
CREATE TABLE pa_restoration_monitoring_network.monitoring_area (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    geometry GEOMETRY
);

-- Crear la tabla para 'sampling_point'
CREATE TABLE pa_restoration_monitoring_network.sampling_point (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    geometry GEOMETRY,
    easting DECIMAL,
    northing DECIMAL,
    horizontal_accuracy DECIMAL,
    vertical_accuracy DECIMAL,
    elevation DECIMAL,
    satellites INTEGER,
    gnss_height DECIMAL,
    corner VARCHAR
);

-- Crear la tabla para 'drain_points'
CREATE TABLE pa_restoration_monitoring_network.drain_points (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    geometry GEOMETRY,
    easting DECIMAL,
    northing DECIMAL,
    horizontal_accuracy DECIMAL,
    vertical_accuracy DECIMAL,
    elevation DECIMAL,
    satellites INTEGER,
    gnss_height DECIMAL
);

-- Crear la tabla para 'photo_points'
CREATE TABLE pa_restoration_monitoring_network.photo_points (
    id SERIAL PRIMARY KEY,
	rmn_id VARCHAR,
    easting DECIMAL,
    northing DECIMAL
);

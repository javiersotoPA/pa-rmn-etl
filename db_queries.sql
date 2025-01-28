DROP SCHEMA  pa_restoration_monitoring_network;
CREATE SCHEMA pa_restoration_monitoring_network;

CREATE TABLE pa_restoration_monitoring_network.desk_study (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    site VARCHAR(255),
    grant_notes VARCHAR,
    condition_category VARCHAR(255),
    aerial_imagery_notes VARCHAR,
    land_use VARCHAR(255),
    land_use_notes VARCHAR,
    land_use_change_notes VARCHAR,
    deer_density_notes VARCHAR,
    herbivore_impact_notes VARCHAR,
    general_notes VARCHAR,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.quadrat_information (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point VARCHAR(255),
    date DATE,
    surveyors VARCHAR(255),
    markers_found VARCHAR(255),
    feature_type VARCHAR(255),
    quadrat_type VARCHAR(255),
    aspect VARCHAR(255),
    peat_depth INT,
    bare_peat DECIMAL(5,2),
    bare_mineral DECIMAL(5,2),
    open_water DECIMAL(5,2),
    litter DECIMAL(5,2),
    trampling VARCHAR(255),
    dung VARCHAR(255),
    trees VARCHAR(255),
    veg_height_1 INT,
    veg_height_2 INT,
    veg_height_3 INT,
    veg_height_4 INT,
    veg_height_5 INT,
    disturbance_notes VARCHAR,
    quadrat_notes VARCHAR,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.vegetation (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point VARCHAR(255),
    species VARCHAR(255),
    cover DECIMAL(5,2),
    notes VARCHAR,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.feature_status_drains (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point VARCHAR(255),
    drain_point VARCHAR(255),
    drain_identifiable BOOLEAN,
    depth VARCHAR(255),
    width VARCHAR(255),
    flow VARCHAR(255),
    bare_peat VARCHAR(255),
    bare_mineral VARCHAR(255),
    open_water VARCHAR(255),
    litter VARCHAR(255),
    vegetation VARCHAR(255),
    dwarf_shrub VARCHAR(255),
    eriophorum VARCHAR(255),
    trichophorum VARCHAR(255),
    molinia VARCHAR(255),
    other_poaceae VARCHAR(255),
    juncus VARCHAR(255),
    sphagnum VARCHAR(255),
    other_moss VARCHAR(255),
    lichen VARCHAR(255),
    block_present VARCHAR(255),
    erosion_around VARCHAR(255),
    erosion_over VARCHAR(255),
    block_trampling VARCHAR(255),
    water_retained VARCHAR(255),
    water_retained_sphagnum VARCHAR(255),
    sediment_retained VARCHAR(255),
    block_vegetation_establishing VARCHAR(255),
    donor BOOLEAN,
    donor_vegetation_establishing VARCHAR(255),
    score VARCHAR(255),
    notes VARCHAR,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.photos (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    title VARCHAR(255),
    date DATE,
    photographer VARCHAR(255),
    bearing INT,
    notes VARCHAR,
    dams_link VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);



CREATE TABLE pa_restoration_monitoring_network.area_level_assessment (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    site VARCHAR(255),
    survey_dates VARCHAR(255),
    surveyors VARCHAR(255),
    weather VARCHAR(255),
    ground_conditions VARCHAR(255),
    nvc_approximate VARCHAR(255),
    nvc_approximate_notes VARCHAR,
    bare_peat VARCHAR(255),
    bare_peat_notes VARCHAR,
    dwarf_shrub VARCHAR(255),
    dwarf_shrub_notes VARCHAR,
    eriophorum VARCHAR(255),
    eriophorum_notes VARCHAR,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.monitoring_area (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    geometry GEOMETRY,
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.sampling_points (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point_id VARCHAR(50),
    easting DECIMAL(10,6),
    northing DECIMAL(10,6),
    horizontal_accuracy DECIMAL(5,2),
    vertical_accuracy DECIMAL(5,2),
    date DATE,
    elevation DECIMAL(5,2),
    satellites INT,
    source VARCHAR(255),
    gnss_height DECIMAL(5,2),
    feature_type VARCHAR(255),
    corner VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);


CREATE TABLE pa_restoration_monitoring_network.feature_status_gullies (
    rmn_id VARCHAR(255),
    grant_id VARCHAR(255),
    visit VARCHAR(255),
    sampling_point VARCHAR(255),
    depth VARCHAR(255),
    width VARCHAR(255),
    side VARCHAR(255),
    angle VARCHAR(255),
    vegetation_establishing BOOLEAN,
    trampling BOOLEAN,
    flow BOOLEAN,
    bare_peat VARCHAR(255),
    bare_mineral VARCHAR(255),
    open_water VARCHAR(255),
    litter VARCHAR(255),
    vegetation VARCHAR(255),
    dwarf_shrub VARCHAR(255),
    eriophorum VARCHAR(255),
    trichophorum VARCHAR(255),
    molinia VARCHAR(255),
    other_poaceae VARCHAR(255),
    juncus VARCHAR(255),
    sphagnum VARCHAR(255),
    other_moss VARCHAR(255),
    lichen VARCHAR(255),
    block_present BOOLEAN,
    erosion_around VARCHAR(255),
    erosion_over VARCHAR(255),
    block_trampling VARCHAR(255),
    water_retained VARCHAR(255),
    water_retained_sphagnum VARCHAR(255),
    sediment_retained VARCHAR(255),
    block_vegetation_establishing VARCHAR(255),
    donor BOOLEAN,
    donor_vegetation_establishing VARCHAR(255),
    score VARCHAR(255),
    notes VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.feature_status_hags (
    rmn_id VARCHAR(255),
    grant_id VARCHAR(255),
    visit VARCHAR(255),
    sampling_point VARCHAR(255),
    height VARCHAR(255),
    angle VARCHAR(255),
    vegetation_establishing BOOLEAN,
    trampling BOOLEAN,
    erosion BOOLEAN,
    donor BOOLEAN,
    donor_vegetation_establishing VARCHAR(255),
    score VARCHAR(255),
    notes VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.feature_status_bare_peat (
    rmn_id VARCHAR(255),
    grant_id VARCHAR(255),
    visit VARCHAR(255),
    sampling_point VARCHAR(255),
    area VARCHAR(255),
    vegetation_establishing BOOLEAN,
    trampling BOOLEAN,
    erosion BOOLEAN,
    bund_present BOOLEAN,
    bund_erosion VARCHAR(255),
    water_retained VARCHAR(255),
    water_retained_sphagnum VARCHAR(255),
    bund_vegetation_establishing VARCHAR(255),
    donor BOOLEAN,
    donor_vegetation_establishing VARCHAR(255),
    score VARCHAR(255),
    notes VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);

CREATE TABLE pa_restoration_monitoring_network.feature_status_forest_to_bog (
    rmn_id VARCHAR(255),
    grant_id VARCHAR(255),
    visit VARCHAR(255),
    sampling_point VARCHAR(255),
    tree_cover VARCHAR(255),
    tree_height VARCHAR(255),
    mulch VARCHAR(255),
    bare_peat VARCHAR(255),
    tree_regen BOOLEAN,
    ground_level BOOLEAN,
    peat_cracking BOOLEAN,
    score VARCHAR(255),
    notes VARCHAR(255),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);



CREATE TABLE pa_restoration_monitoring_network.drain_points (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point_id VARCHAR(50),
    easting DECIMAL(10,6),
    northing DECIMAL(10,6),
    horizontal_accuracy DECIMAL(5,2),
    vertical_accuracy DECIMAL(5,2),
    date DATE,
    elevation DECIMAL(5,2),
    satellites INT,
    drain_point_id VARCHAR(255),
    gnss_height DECIMAL(5,2),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);


CREATE TABLE pa_restoration_monitoring_network.fpp_points (
    rmn_id VARCHAR(10),
    grant_id VARCHAR(10),
    visit VARCHAR(50),
    sampling_point_id VARCHAR(50),
    easting DECIMAL(10,6),
    northing DECIMAL(10,6),
    horizontal_accuracy DECIMAL(5,2),
    vertical_accuracy DECIMAL(5,2),
    date DATE,
    elevation DECIMAL(5,2),
    satellites INT,
    drain_point_id VARCHAR(255),
    gnss_height DECIMAL(5,2),
    importe_by VARCHAR(255),
    updated_by VARCHAR(255),
    updated_date DATE,
    import_date DATE
);






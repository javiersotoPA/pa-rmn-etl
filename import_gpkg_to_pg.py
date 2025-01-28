"""
Import gpkg to postgres This script takes the spatial data geopackage and inserts the data into postgres,
adding the relevant grant ID at the same time - any constraint failures will be feedback to the user
"""

import argparse

import psycopg2
from osgeo import ogr
from psycopg2 import sql

from config import config


def connect_postgres():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:

        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        return conn

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)


def create_field_list(layer, schema_name):
    """Go through the layer and extract each of the field names"""

    field_list = []
    layer_defn = layer.GetLayerDefn()

    # Add the geometry column, if there is one!
    geom_col = layer.GetGeometryColumn()
    if not geom_col == "":
        field_list.append(geom_col)

    # Add the rest of the fields from the geopackage
    for i in range(layer_defn.GetFieldCount()):
        field_defn = layer_defn.GetFieldDefn(i).GetName()
        field_list.append(field_defn)

    # add the grant_id/feasibility_study_id field
    if schema_name in ["pa_final_report", "pa_application", "test_data_model"]:
        field_list.append("grant_id")
    if schema_name in ["pa_feasibility"]:
        field_list.append("fs_id")

    return field_list


def create_values_string(layer, grant_id):
    values_string = ""

    # for each feature
    for j in range(1, layer.GetFeatureCount() + 1):

        values = []
        # get the next feature (**can't use the indexed GetNextFeature(fid) as the fid does not necessarily start at
        # 1 and increment by 1)
        feature = layer.GetNextFeature()

        # check it's not null
        if feature is not None:

            geom = feature.GetGeometryRef()
            if geom is not None:
                values += ["st_geomfromtext('" + str(geom) + "',27700)"]

            for key in feature.keys():
                # Get the value for each field and add it to the values array:

                fld_defn = feature.GetFieldDefnRef(feature.GetFieldIndex(key))
                if (
                    fld_defn.GetType() == ogr.OFTInteger
                    and fld_defn.GetSubType() == ogr.OFSTBoolean
                ):
                    val = bool(feature.GetField(key))
                else:
                    val = feature.GetField(key)

                # Postgres strings must be enclosed with single quotes
                if type(val) == str:
                    # escape apostrophes with two single quotations
                    val = val.replace("'", "''")  # type: ignore
                    val = "'" + val + "'"
                if val is None:
                    val = "NULL"

                values += [str(val)]
            # add the grant_id to the feature
            values += ["'" + grant_id + "'"]
            # make a string surrounded by brackets for each feature's values
            values_string += "(" + ",".join(values) + "),\n"
    # remove the last comma and replace with a semi-colon - the end of the sql query
    values_string = values_string[:-2] + ";"
    return values_string


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", help="Name of the geopackage to be imported")
    parser.add_argument(
        "grantID",
        help="The grant ID or feasibility ID for the spatial data - ensure this is already present in the database ("
        "pa_metadata.grant_reference table or pa_metadata.feasibility_reference table)",
    )
    parser.add_argument(
        "schemaname",
        help="The name of the schema to add the data into - ie pa_final_report or pa_application",
        choices=[
            "pa_final_report",
            "pa_application",
            "pa_feasibility",
            "test_data_model",
        ],
    )
    parser.add_argument(
        "-y", "--year_end", required=False, help="The financial year end of the project"
    )

    args = parser.parse_args()

    if args.schemaname == "pa_final_report":
        if args.year_end is None:
            parser.error(
                "For pa_final_report a financal year end is required - e.g. -y 2023"
            )

    gpkg_filename = args.filename
    grant_id = args.grantID
    schema_name = args.schemaname
    year_end = args.year_end

    # assign relevant metadata schema
    if schema_name in ["pa_final_report", "pa_application", "pa_feasibility"]:
        metadata_schema = "pa_metadata"
    else:
        metadata_schema = "test_data_model"

    gpkg_driver = ogr.GetDriverByName("GPKG")
    pg_conn = connect_postgres()

    if schema_name in ["pa_final_report", "pa_application", "pa_feasibility", "test_data_model"]:
        with pg_conn:
            with pg_conn.cursor() as cur:
                # Check that the grant reference is present in the database, and if not, prompt user to do something
                # about it.
                if schema_name in ["pa_final_report", "pa_application", "test_data_model"]:
            
                    cur.execute(
                        "SELECT count(*) from {}.grant_reference where grant_id = %s".format(
                            metadata_schema
                        ),
                        (grant_id,),
                    )
                    count_grant_id = cur.fetchone()
                else:
                    cur.execute(
                    "SELECT count(*) from {}.feasibility_reference where fs_id = %s".format(
                        metadata_schema
                    ),
                    (grant_id,),
                    )
                    count_grant_id = cur.fetchone()
               


        with pg_conn:
            with pg_conn.cursor() as cur:
                # retrieve list of tables from database for subsequent filtering of gpkg layers
                # note hardcoded 'pa_final_report' as test db contains meta and lu tables
                cur.execute(
                    "SELECT table_name FROM information_schema.tables WHERE table_schema='pa_final_report' "
                    "AND table_type='BASE TABLE'"
                )
                result = cur.fetchall()
                table_list = [i[0] for i in result]

    if schema_name in ["pa_final_report", "test_data_model"]:
        with pg_conn:
            with pg_conn.cursor() as cur:
                # Check that the grant reference is present in the database, and if not, prompt user to do something
                # about it.
                query = sql.SQL(
                    "UPDATE {schema}.grant_reference SET financial_year_end = %s WHERE grant_id = %s"
                ).format(schema=sql.Identifier(metadata_schema))
                cur.execute(
                    query,
                    (
                        year_end,
                        grant_id,
                    ),
                )

    if count_grant_id[0] > 0:
        with pg_conn:
            with pg_conn.cursor() as cur:

                # Open geopackage
                # gpkg = ogr.Open(gpkg_filename)
                gpkg = gpkg_driver.Open(gpkg_filename)
                # For each layer in the geopackage
                for layer in gpkg:
                    

                    table_name = layer.GetName()
                    #print(table_name)

                    # check there are features in the layer (count needs to be > 1 because there is a 'spatial
                    # filter' which is always included in the count - see ogr.py line 1517)
                    if layer.GetFeatureCount() > 0 and table_name in table_list:
                        print(
                            "Layer being processed: {}; feature count = {}".format(
                                table_name, layer.GetFeatureCount()
                            )
                        )
                        # Get the list of fields for the layer:
                        field_list = create_field_list(layer, schema_name)
                        # Get the features from the layer and insert them into the database, adding in grant ref:

                        values_string = create_values_string(layer, grant_id)

                        sql_string = cur.mogrify(
                            "INSERT INTO {}.{} ({})\n VALUES {}".format(
                                schema_name,
                                table_name,
                                ",".join(field_list),
                                values_string,
                            )
                        )
                        # print(sql_string)
                        cur.execute(sql_string)

        # with pg_conn:
        #    with pg_conn.cursor() as cur:
        #        cur.execute(final_transaction_sql)

    else:
        print(
            "The grant reference {} was not found in the database, please ensure it is added to the grant_reference "
            "table".format(grant_id)
        )

    pg_conn.close()


if __name__ == "__main__":
    main()

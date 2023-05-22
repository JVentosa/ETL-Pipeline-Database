
import sys
import pandas as pd
import pymysql.cursors
import config
import numpy as np
import psycopg2

#reset.py created to quickly erase tables in postgresql application


#Create PostgreSQL Table for Report Contents
def report_content_table(my_cursor, pg_cursor, pg_cnx):

    query = """
create table if not exists report_content
(
    id             serial      not null
        constraint report_content_pkey
            primary key,
    current_status varchar(100) not null,
    rid            integer      not null
        constraint rid_report_content__id_fk
            references report,
    hid            integer      not null
        constraint hid_report_content__id_fk
            references hospital,
    outid          integer      not null
        constraint outid_report_content___fk
            references outpatient_revenue,
    visid          integer      not null
        constraint visid_report_content___fk
            references visits,
    expid          integer      not null
        constraint expid_report_content___fk
            references expenses,
    inid           integer      not null
        constraint inid_report_content___fk
            references inpatient_revenue,
    utilid         integer      not null
        constraint utilid_report_content___fk_
            references utilization,
    patid          integer      not null
        constraint patid_report_content___fk
            references patient_days,
    disid          integer      not null
        constraint disid_report_content___fk
            references discharges
);
"""
    pg_cursor.execute(query)

    # This is from mysql
    # Selects the id, current_status, report_id and hospitaL_id from mysql
    report_query = "select id as rcid, current_status, rid, hid from report_content;"
    my_cursor.execute(report_query)
    report_content_data = my_cursor.fetchall()

    # Now that we have report_content we can go one by one and create everything for each report:
    for row in report_content_data:
        rcid = row[0]
        current_status = row[1]
        report_id = row[2]
        hospital_id = row[3]

        # This is from mysql
        outpatient_revenue_query = "select medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care from outpatient_revenue where rcid = %s"
        # assuming 0 is the rcid
        my_cursor.execute(outpatient_revenue_query, rcid)
        outpatient_revenue_data = my_cursor.fetchall()[0]
       
        # This is from postgresql
        outpatient_revenue_query = "insert into outpatient_revenue (medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care) values ( %s, %s, %s, %s) returning id;"
        pg_cursor.execute(outpatient_revenue_query, outpatient_revenue_data)
        outpatient_revenue_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        visits_query = "select medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care from visits where rcid = %s"
        # assuming 0 is the rcid
        my_cursor.execute(visits_query, rcid)
        visits_data = my_cursor.fetchall()[0]

        # This is from postgresql
        visits_query = "insert into visits (medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care) values ( %s, %s, %s, %s) returning id;"
        pg_cursor.execute(visits_query, visits_data)
        visits_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        expenses_query = "select operational, professional from expenses where rcid = %s"
        
        # assuming 0 is the rcid
        my_cursor.execute(expenses_query, rcid) 
        expenses_data = my_cursor.fetchall()[0]

        # This is from postgresql
        expenses_query = "insert into expenses (operational, professional) values ( %s, %s) returning id;"
        pg_cursor.execute(expenses_query, expenses_data)
        expenses_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        inpatient_revenue_query = "select medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care from inpatient_revenue where rcid = %s"
        # assuming 0 is the rcid
        my_cursor.execute(inpatient_revenue_query, rcid)
        inpatient_revenue_data = my_cursor.fetchall()[0]

        # This is from postgresql
        inpatient_revenue_query = "insert into inpatient_revenue (medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care) values ( %s, %s, %s, %s) returning id;"
        pg_cursor.execute(inpatient_revenue_query, inpatient_revenue_data)
        inpatient_revenue_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        utilization_query = "select available_beds, staffed_beds, license_beds from utilization where rcid = %s"
        
        # assuming 0 is the rcid
        my_cursor.execute(utilization_query, rcid)
        utilization_data = my_cursor.fetchall()[0]

        # This is from postgresql
        utilization_query = "insert into utilization (available_beds, staffed_beds, license_beds) values ( %s, %s, %s) returning id;"
        pg_cursor.execute(utilization_query, utilization_data)
        utilization_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        patient_days_query = "select medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care from patient_days where rcid = %s"
        # assuming 0 is the rcid
        my_cursor.execute(patient_days_query, rcid)
        patient_days_data = my_cursor.fetchall()[0]

        # This is from postgresql
        patient_days_query = "insert into patient_days (medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care) values ( %s, %s, %s, %s) returning id;"
        pg_cursor.execute(patient_days_query, patient_days_data)
        patient_days_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################
        # This is from mysql
        discharges_query = "select medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care from discharges where rcid = %s"
        # assuming 0 is the rcid
        my_cursor.execute(discharges_query, rcid)
        discharges_data = my_cursor.fetchall()[0]

        # This is from postgresql
        discharges_query = "insert into discharges (medicare_traditional, medicare_care,\
                                    medi_traditional, medi_care) values ( %s, %s, %s, %s) returning id;"
        pg_cursor.execute(discharges_query, discharges_data)
        discharges_id = pg_cursor.fetchall()[0]
        ##########################################################################################################################

        # This is from postgresql
        #Inserts ALL ids into Report_Content Table
        report_query = "Insert into report_content (current_status, rid, hid, outid, visid, expid, inid, utilid,\
                        patid, disid) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        pg_cursor.execute(report_query, (current_status, report_id, hospital_id, outpatient_revenue_id, visits_id, expenses_id,\
                                         inpatient_revenue_id, utilization_id, patient_days_id, discharges_id))
        
    pg_cnx.commit()


# Create PostgreSQL Table for Hospitals
def hospital_tables(my_cursor, pg_cursor, pg_cnx):
    query = "select id, name, year_qtr, county,\
                               planning_area, control_type, type, phone, address,\
                               city, zipcode, ceo from hospital;"
    my_cursor.execute(query)
    table = my_cursor.fetchall()

    query = """   
        create table if not exists hospital
(
    id         integer not null
        constraint hospital_pkey
            primary key,
    name          varchar(100) not null,
    year_qtr       integer not null,
    county        varchar(100) not null,
    planning_area integer      not null,
    control_type  varchar(100) not null,
    type          varchar(100) not null,
    phone         varchar(100) not null,
    address       varchar(100) not null,
    city          varchar(100) not null,
    zipcode       varchar(100) not null,
    ceo           varchar(100) not null
);
    TRUNCATE Hospital CASCADE;
"""
    pg_cursor.execute(query)
    inserting = """
                    INSERT INTO hospital (id, name, year_qtr, county, planning_area, control_type,\
                                        type, phone, address, city, zipcode, ceo)\
                 values (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s) RETURNING id"""
    pg_cursor.executemany(inserting, table)
    pg_cnx.commit()


# Create PostgreSQL Table for Reports
def report_table(my_cursor, pg_cursor, pg_cnx):
    query = 'Select id, year, quarter, start_date, end_date from report'
    my_cursor.execute(query)
    table = my_cursor.fetchall()

    query = """   
        create table if not exists report
(
    id         serial not null
        constraint report_pkey
            primary key,
    year       integer not null,
    quarter    integer not null,
    start_date date    not null,
    end_date   date    not null
);
"""
    pg_cursor.execute(query)
    inserting = """INSERT INTO report (id, year, quarter, start_date, end_date)\
                 values (%s, %s, %s, %s, %s)"""
    pg_cursor.executemany(inserting, table)
    pg_cnx.commit()


# Create PostgreSQL Table for Discharges
def discharges_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists discharges
(
    id                   serial not null
        constraint discharges_pkey
            primary key,
    medicare_traditional integer not null,
    medicare_care        integer not null,
    medi_traditional     integer not null,
    medi_care            integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Expenses
def expenses_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists expenses
(
    id            serial not null
        constraint expenses_pkey
            primary key,
    operational  bigint  not null,
    professional integer not null
); 
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Inpatient Revenue
def inpatient_revenue_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists inpatient_revenue
(
    id                   serial not null
        constraint inpatient_revenue_pkey
            primary key,
    medicare_traditional integer not null,
    medicare_care        integer not null,
    medi_traditional     integer not null,
    medi_care            integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Outpatient Revenue
def outpatient_revenue_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists outpatient_revenue
(
    id                   serial not null        
        constraint outpatient_revenue_pkey
            primary key,
    medicare_traditional integer not null,
    medicare_care        integer not null,
    medi_traditional     integer not null,
    medi_care            integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Patient Days
def patient_days_table(pg_cursor, pg_cnx):

    query = """   
        create table if not exists patient_days
(
    id                   serial not null
        constraint patient_days_pkey
            primary key,
    medicare_traditional integer not null,
    medicare_care        integer not null,
    medi_traditional     integer not null,
    medi_care            integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Staff
def staff_table(my_cursor, pg_cursor, pg_cnx):
    query = 'select hid, productive_hours_per_patient,\
                            productive_hours, position from staff'
    my_cursor.execute(query)
    table = my_cursor.fetchall()

    query = """   
        create table if not exists staff
(
    id                           serial      not null
        constraint staff_pkey
            primary key,
    hid                          integer     not null
        constraint hid_staff___fk
            references hospital,
    productive_hours_per_patient integer      not null,
    productive_hours             integer      not null,
    position                     varchar(100) not null
);
"""
    pg_cursor.execute(query)

    query = """
        INSERT into staff (hid, productive_hours_per_patient,\
                            productive_hours, position) VALUES (%s, %s, %s, %s) returning id;
            """
    pg_cursor.executemany(query, table)
    pg_cnx.commit()


# Create PostgreSQL Table for Utilization
def utilization_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists utilization
(
    id             serial not null
        constraint utilization_pkey
            primary key,
    available_beds integer not null,
    staffed_beds   integer not null,
    license_beds   integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()


# Create PostgreSQL Table for Visits
def visits_table(pg_cursor, pg_cnx):
    query = """   
        create table if not exists visits
(
    id                   serial not null
        constraint visits_pkey
            primary key,
    medicare_traditional integer not null,
    medicare_care        integer not null,
    medi_traditional     integer not null,
    medi_care            integer not null
);
"""
    pg_cursor.execute(query)
    pg_cnx.commit()



# Connects to MySQL Database
try:
    my_cnx = pymysql.connect(
        user=config.config_db['user'],
        password=config.config_db['password'],
        host=config.config_db['host'],
        database=config.config_db['database'],
        port=config.config_db['port']
    )
    #print("Connected to MySQL database")
except pymysql.Error as err:
    print(f"Error: {err}")
    sys.exit(1)

# MYSQL Cursor for parsing
my_cursor = my_cnx.cursor()

# Connects to Postgres Database
try:
    pg_cnx = psycopg2.connect(
        user=config.config_warehouse['user'],
        password=config.config_warehouse['password'],
        host=config.config_warehouse['host'],
        database=config.config_warehouse['database'],
        port=config.config_warehouse['port']
    )
    #print("Connected to Postgres database")
except psycopg2.Error as err:
    print(f"Error:  {err}")
    sys.exit(1)

#Postgres Cursor for PARSING
pg_cursor = pg_cnx.cursor()

expenses_table(pg_cursor, pg_cnx)
discharges_table(pg_cursor, pg_cnx)
inpatient_revenue_table(pg_cursor, pg_cnx)
outpatient_revenue_table(pg_cursor, pg_cnx)
patient_days_table(pg_cursor, pg_cnx)
utilization_table(pg_cursor, pg_cnx)
visits_table(pg_cursor, pg_cnx)
hospital_tables(my_cursor, pg_cursor, pg_cnx)
report_table(my_cursor, pg_cursor, pg_cnx)
staff_table(my_cursor, pg_cursor, pg_cnx)
report_content_table(my_cursor, pg_cursor, pg_cnx)
pg_cnx.commit()
pg_cnx.close()
my_cnx.close()
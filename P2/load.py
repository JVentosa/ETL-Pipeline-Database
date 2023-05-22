import os
import csv
import sys
import pandas as pd
import mysql.connector
import config
import numpy as np

# Function to read data from a CSV file.
def read_csv(filename):
    df = pd.read_csv(filename)
    df = df.replace(np.nan, '', regex=True)
    return df

# Function to insert data into a table.
def insert_data_reports(cursor, data):
    # Build the SQL statement.
    # print("Inserting data")
    for index, row in data.iterrows():
        # print("Inserting into hospital: ", (row['hid'], row['name'], row['year_qtr'], row['county_name'], row['planning_area'], row['type_cntrl'], row['type_hosp'], row['phone'], row['address'], row['city'], row['zip_code'], row['ceo']))

        # print ("Checking if existing hospital")
        cursor.execute(f"select * from hospital where id = %s", (row['hid'],))
        if not (cursor.fetchone()):
            statement = f"INSERT INTO hospital (id, name, year_qtr, county, planning_area, control_type, type, phone, address, city, zipcode, ceo) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(statement, (row['hid'], row['name'], row['year_qtr'], row['county_name'], row['planning_area'],
                           row['type_cntrl'], row['type_hosp'], row['phone'], row['address'], row['city'], row['zip_code'], row['ceo']))
        else:
            statement = f"select year_qtr from hospital where id = %s;"
            cursor.execute(statement, (row['hid'],))
            year_qtr = cursor.fetchone()[0]
            year = year_qtr // 10
            qtr = year_qtr % 10

            if (year < (row['year_qtr']//10) or (year == (row['year_qtr']//10) and qtr < (row['year_qtr'] % 10))):
                # If the year_qtr is more recent, update year_qtr
                # print("Querying for latest information...")

                updateStatement = f"Update hospital set year_qtr = %s where id = %s;"
                cursor.execute(updateStatement, (row['year_qtr'], row['hid']))

            # If there are any null values, update them with information from current row
            # print("Updating null values in old record")
            column_names = {'hid': 'id', 'name': 'name', 'year_qtr': 'year_qtr', 'county_name': 'county',
                            'planning_area': 'planning_area', 'type_cntrl': 'control_type', 'type_hosp': 'type',
                            'phone': 'phone', 'address': 'address', 'city': 'city', 'zip_code': 'zipcode', 'ceo': 'ceo'}

            for key, value in column_names.items():
                qry = f"select %s from hospital where id = %s;"
                cursor.execute(qry, (value, row['hid']))
                attribute = cursor.fetchone()[0]
                if ((attribute == "" or attribute == " ") and (row[key] != "" or row[key] != " ")):
                    updateStatement = f"Update hospital set %s = %s where id = %s;"
                    cursor.execute(updateStatement,
                                   (value, row[key], row['hid']))

        statement = f"INSERT INTO report (year, quarter, start_date, end_date) VALUES (%s, %s, %s, %s);"

        # Extract the year from the "year_qtr" column
        year = row['year_qtr']//10
        # Extract the quarter from the "year_qtr" column
        quarter = row['year_qtr'] % 10
        cursor.execute(
            f"select id from report where year = %s and quarter = %s", (year, quarter))
        res = cursor.fetchone()
        if not (res):
            # print("Inserting into report: ", (year, quarter, row['start_date'], row['end_date']))
            cursor.execute(statement, (year, quarter,
                           row['start_date'], row['end_date']))
            # Get last inserted id from reports
            cursor.execute("SELECT LAST_INSERT_ID();")
            rid = cursor.fetchone()[0]
        else:
            rid = res[0]

        # print("RID:", rid)
        # print("Inserting into report_content: ", (row['hstatus'], rid, row['hid']))
        statement = f"INSERT INTO report_content (current_status, rid, hid) VALUES (%s, %s, %s);"
        cursor.execute(statement, (row['hstatus'], rid, row['hid']))
        # Get last inserted id from report_content
        cursor.execute("SELECT LAST_INSERT_ID();")
        rcid = cursor.fetchone()[0]
        # print("RCID:", rcid)

        # print("Inserting into discharges:", (rcid, row['dis_medicare_tradicional'], row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))
        statement = f"INSERT INTO discharges (rcid, medicare_traditional, medicare_care, medi_traditional, medi_care) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (rcid, row['dis_medicare_tradicional'],
                       row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))

        # print("Inserting into expenses:", (rcid, row['operational_expenses'], row['professional_expenses']))
        statement = f"INSERT INTO expenses (rcid, operational, professional) VALUES (%s, %s, %s)"
        cursor.execute(
            statement, (rcid, row['operational_expenses'], row['professional_expenses']))

        # print("Inserting into inpatient_revenue:", (rcid, row['dis_medicare_tradicional'], row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))
        statement = f"INSERT INTO inpatient_revenue (rcid, medicare_traditional, medicare_care, medi_traditional, medi_care) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (rcid, row['dis_medicare_tradicional'],
                       row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))

        # print("Inserting into outpatient_revenue:", (rcid, row['dis_medicare_tradicional'], row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))
        statement = f"INSERT INTO outpatient_revenue (rcid, medicare_traditional, medicare_care, medi_traditional, medi_care) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (rcid, row['dis_medicare_tradicional'],
                       row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))

        # print("Inserting into patient_days:", (rcid, row['dis_medicare_tradicional'], row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))
        statement = f"INSERT INTO patient_days (rcid, medicare_traditional, medicare_care, medi_traditional, medi_care) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (rcid, row['dis_medicare_tradicional'],
                       row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))

        # print("Inserting into utilization:", (rcid, row['avl_beds'], row['stf_beds'], row['lic_beds']))
        statement = f"INSERT INTO utilization (rcid, available_beds, staffed_beds, license_beds) VALUES (%s, %s, %s, %s)"
        cursor.execute(
            statement, (rcid, row['avl_beds'], row['stf_beds'], row['lic_beds']))

        # print("Inserting into visits:", (rcid, row['dis_medicare_tradicional'], row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))
        statement = f"INSERT INTO visits (rcid, medicare_traditional, medicare_care, medi_traditional, medi_care) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(statement, (rcid, row['dis_medicare_tradicional'],
                       row['dis_medicare_care'], row['dis_medi_tradicional'], row['dis_medi_care']))


def insert_data_staff(cursor, data):

    for index, row in data.iterrows():
        # print("Inserting into staff:", (row["facility_id"],row["productive_hours_per_patient"],row["productive_hours"],row["position"]))
        cursor.execute(f"select * from hospital where id = %s",
                       (row['facility_id'],))
        if (cursor.fetchone()):
            cursor.execute("select * from staff where hid = %s AND productive_hours_per_patient = %s AND productive_hours = %s AND position = %s",
                           (row['facility_id'], row["productive_hours_per_patient"], row["productive_hours"], row["position"]))
            if not cursor.fetchone():
                statement = f"INSERT INTO staff ( hid, productive_hours_per_patient, productive_hours, position) VALUES (%s, %s, %s, %s)"
                cursor.execute(
                    statement, (row["facility_id"], row["productive_hours_per_patient"], row["productive_hours"], row["position"]))

# connect to mysql function
try:
    cnx = mysql.connector.connect(
        user=config.config_db['user'],
        password=config.config_db['password'],
        host=config.config_db['host'],
        database=config.config_db['database'],
        port=config.config_db['port']
    )
    # print("Connected to the database")
except mysql.connector.Error as err:
    # print(f"Error: {err}")
    cnx.close()
    sys.exit(1)

# add cursor to parse
cursor = cnx.cursor()

# Process the reports dataset.
reports_folder = sys.argv[1]
for filename in os.listdir(reports_folder):
    # print("Processing:", filename)
    if filename.endswith('.csv'):
        data = read_csv(os.path.join(reports_folder, filename))
        insert_data_reports(cursor, data)

# Process the staff dataset.
staff_folder = sys.argv[2]
for filename in os.listdir(staff_folder):
    if filename.endswith('.csv'):
        data = read_csv(os.path.join(staff_folder, filename))
        insert_data_staff(cursor, data)

# Commit the changes and close the connection.
cnx.commit()
cursor.close()
cnx.close()

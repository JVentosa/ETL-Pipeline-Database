-- This file contains the definitions of the tables used.
--
--
-- Hospital table
create table if not exists hospital
(
    id            int          not null
        primary key,
    name          varchar(100) not null,
    year_qtr      int          not null,
    county        varchar(100) not null,
    planning_area int          not null,
    control_type  varchar(100) not null,
    type          varchar(100) not null,
    phone         varchar(100) not null,
    address       varchar(100) not null,
    city          varchar(100) not null,
    zipcode       varchar(100) not null,
    ceo           varchar(100) not null
);

-- Report table 
create table if not exists report
(
    id         int auto_increment not null
        primary key,
    year       int  not null,
    quarter    int  not null,
    start_date date not null,
    end_date   date not null
);

-- Report Content table
create table if not exists report_content
(
    id             int auto_increment not null
        primary key,
    current_status varchar(100) not null,
    rid            int          not null,
    hid            int          not null,
    constraint report_content_hospital_id_fk
        foreign key (hid) references hospital (id),
    constraint rid
        foreign key (rid) references report (id)
);

-- Discharges table 
create table if not exists discharges
(
    id                   int auto_increment not null
        primary key,
    rcid                 int not null,
    medicare_traditional int not null,
    medicare_care        int not null,
    medi_traditional     int not null,
    medi_care            int not null,
    constraint discharges_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Expenses table
create table if not exists expenses
(
    rcid         int    not null,
    operational  bigint not null,
    professional int    not null,
    constraint expenses_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Inpatient Revenue table 
create table if not exists inpatient_revenue
(
    rcid                 int not null,
    medicare_traditional int not null,
    medicare_care        int not null,
    medi_traditional     int not null,
    medi_care            int not null,
    constraint inpatient_revenue_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Outpatient Revenue table 
create table if not exists outpatient_revenue
(
    rcid                 int not null,
    medicare_traditional int not null,
    medicare_care        int not null,
    medi_traditional     int not null,
    medi_care            int not null,
    constraint outpatient_revenue_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Patient Days table
create table if not exists patient_days
(
    rcid                 int not null,
    medicare_traditional int not null,
    medicare_care        int not null,
    medi_traditional     int not null,
    medi_care            int not null,
    constraint patient_days_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Staff table
create table if not exists staff
(
    id                           int auto_increment          not null
        primary key,
    hid                          int          not null,
    productive_hours_per_patient float          not null,
    productive_hours             int          not null,
    position                     varchar(100) not null,
    constraint hid
        foreign key (hid) references hospital (id)
);

-- Utilization table 
create table if not exists utilization
(
    rcid           int not null,
    available_beds int not null,
    staffed_beds   int not null,
    license_beds   int not null,
    constraint utilization_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

-- Visits table
create table if not exists visits
(
    rcid                 int not null,
    medicare_traditional int not null,
    medicare_care        int not null,
    medi_traditional     int not null,
    medi_care            int not null,
    constraint visits_report_content_id_fk
        foreign key (rcid) references report_content (id)
);

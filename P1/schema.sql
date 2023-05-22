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


--Star schema generated with DataGrip
--Commented as in now

-- create table hospital
-- (
--     id            integer      not null
--         constraint hospital_pkey
--             primary key,
--     name          varchar(100) not null,
--     year_qtr      integer      not null,
--     county        varchar(100) not null,
--     planning_area integer      not null,
--     control_type  varchar(100) not null,
--     type          varchar(100) not null,
--     phone         varchar(100) not null,
--     address       varchar(100) not null,
--     city          varchar(100) not null,
--     zipcode       varchar(100) not null,
--     ceo           varchar(100) not null
-- );

-- alter table hospital
--     owner to postgres;

-- create table report
-- (
--     id         integer not null
--         constraint report_pkey
--             primary key,
--     year       integer not null,
--     quarter    integer not null,
--     start_date date    not null,
--     end_date   date    not null
-- );

-- alter table report
--     owner to postgres;

-- create table expenses
-- (
--     id           integer not null
--         constraint expenses_pkey
--             primary key,
--     operational  bigint  not null,
--     professional integer not null
-- );

-- alter table expenses
--     owner to postgres;

-- create table outpatient_revenue
-- (
--     id                   integer not null
--         constraint outpatient_revenue_pkey
--             primary key,
--     medicare_traditional integer not null,
--     medicare_care        integer not null,
--     medi_traditional     integer not null,
--     medi_care            integer not null
-- );

-- alter table outpatient_revenue
--     owner to postgres;

-- create table discharges
-- (
--     id                   integer not null
--         constraint discharges_pkey
--             primary key,
--     medicare_traditional integer not null,
--     medicare_care        integer not null,
--     medi_traditional     integer not null,
--     medi_care            integer not null
-- );

-- alter table discharges
--     owner to postgres;

-- create table utilization
-- (
--     id             integer not null
--         constraint utilization_pkey
--             primary key,
--     available_beds integer not null,
--     staffed_beds   integer not null,
--     license_beds   integer not null
-- );

-- alter table utilization
--     owner to postgres;

-- create table visits
-- (
--     id                   integer not null
--         constraint visits_pkey
--             primary key,
--     medicare_traditional integer not null,
--     medicare_care        integer not null,
--     medi_traditional     integer not null,
--     medi_care            integer not null
-- );

-- alter table visits
--     owner to postgres;

-- create table patient_days
-- (
--     id                   integer not null
--         constraint patient_days_pkey
--             primary key,
--     medicare_traditional integer not null,
--     medicare_care        integer not null,
--     medi_traditional     integer not null,
--     medi_care            integer not null
-- );

-- alter table patient_days
--     owner to postgres;

-- create table inpatient_revenue
-- (
--     id                   integer not null
--         constraint inpatient_revenue_pkey
--             primary key,
--     medicare_traditional integer not null,
--     medicare_care        integer not null,
--     medi_traditional     integer not null,
--     medi_care            integer not null
-- );

-- alter table inpatient_revenue
--     owner to postgres;

-- create table staff
-- (
--     id                           integer      not null
--         constraint staff_pkey
--             primary key,
--     hid                          integer      not null
--         constraint hid_staff___fk
--             references hospital,
--     productive_hours_per_patient integer      not null,
--     productive_hours             integer      not null,
--     position                     varchar(100) not null
-- );

-- alter table staff
--     owner to postgres;

-- create table report_content
-- (
--     id             integer      not null
--         constraint report_content_pkey
--             primary key,
--     current_status varchar(100) not null,
--     rid            integer      not null
--         constraint rid_report_content__id_fk
--             references report,
--     hid            integer      not null
--         constraint hid_report_content__id_fk
--             references hospital,
--     outid          integer      not null
--         constraint outid_report_content___fk
--             references outpatient_revenue,
--     visid          integer      not null
--         constraint visid_report_content___fk
--             references visits,
--     expid          integer      not null
--         constraint expid_report_content___fk
--             references expenses,
--     inid           integer      not null
--         constraint inid_report_content___fk
--             references inpatient_revenue,
--     utilid         integer      not null
--         constraint utilid_report_content___fk_
--             references utilization,
--     patid          integer      not null
--         constraint patid_report_content___fk
--             references patient_days,
--     disid          integer      not null
--         constraint disid_report_content___fk
--             references discharges
-- );

-- alter table report_content
--     owner to postgres;


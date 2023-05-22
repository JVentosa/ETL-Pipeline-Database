--Star schema generated with DataGrip

create table if not exists hospital
(
    id            integer      not null
        constraint hospital_pkey
            primary key,
    name          varchar(100) not null,
    year_qtr      integer      not null,
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

-- alter table hospital
--     owner to postgres;

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

-- alter table report
--     owner to postgres;

create table if not exists expenses
(
    id           serial not null
        constraint expenses_pkey
            primary key,
    operational  bigint  not null,
    professional integer not null
);

-- alter table expenses
--     owner to postgres;

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

-- alter table outpatient_revenue
--     owner to postgres;

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

-- alter table discharges
--     owner to postgres;

create table if not exists utilization
(
    id             serial not null
        constraint utilization_pkey
            primary key,
    available_beds integer not null,
    staffed_beds   integer not null,
    license_beds   integer not null
);

-- alter table utilization
--     owner to postgres;

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

-- alter table visits
--     owner to postgres;

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

-- alter table patient_days
--     owner to postgres;

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

-- alter table inpatient_revenue
--     owner to postgres;

create table if not exists staff
(
    id                           serial      not null
        constraint staff_pkey
            primary key,
    hid                          integer      not null
        constraint hid_staff___fk
            references hospital,
    productive_hours_per_patient integer      not null,
    productive_hours             integer      not null,
    position                     varchar(100) not null
);

-- alter table staff
--     owner to postgres;

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

-- alter table report_content
--     owner to postgres;

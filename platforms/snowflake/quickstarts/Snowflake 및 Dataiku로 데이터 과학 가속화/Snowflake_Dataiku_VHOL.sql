-- This SQL file is for the Hands On Lab Guide for the 30-day free Snowflake trial account
-- The numbers below correspond to the sections of the Lab Guide in which SQL is to be run in a Snowflake worksheet

/* *********************************************************************************** */
/* *** MODULE 4  ********************************************************************* */
/* *********************************************************************************** */

-- 4.2.8
use role SYSADMIN;
use database COVID19;
use warehouse COMPUTE_WH;

select country_region, sum(cases), case_type, date
from public.jhu_covid_19
where case_type='Confirmed'
  and country_region in ('Germany','United Kingdom', 'France', 'Italy', 'Spain', 'Netherlands', 'Poland', 'Sweden')
group by date, country_region, case_type;

-- 4.2.11
select country_region, sum(cases), case_type, date
from public.jhu_covid_19
where case_type='Active'
  and country_region in ('Germany','United Kingdom', 'France', 'Italy', 'Spain', 'Netherlands', 'Poland', 'Sweden')
group by date, country_region, case_type;

-- 4.3.1
-- If you did not create the COVID19 database from the Data Marketplace, un-comment and run the following three commands:
-- use role accountadmin;
-- create or replace database covid19 from share starschema.covid19;
-- grant imported privileges on database covid19 to public;

use role PC_DATAIKU_ROLE;
use database PC_DATAIKU_DB;
create or replace view JHU_COVID_19 as select * from COVID19.PUBLIC.JHU_COVID_19;
create or replace view GOOG_GLOBAL_MOBILITY_REPORT as select * from COVID19.PUBLIC.GOOG_GLOBAL_MOBILITY_REPORT;

/* *********************************************************************************** */
/* *** MODULE 6  ********************************************************************* */
/* *********************************************************************************** */

-- 6.1.1
use role sysadmin;
use warehouse compute_wh;
use database pc_dataiku_db;

-- 6.1.2
show tables like '%scored%';
select * from "COVID19_TEST_SCORED_space-3a316aed-dku_node-df3ee930";

-- 6.2.2
use role sysadmin;
use warehouse compute_wh;
use database pc_dataiku_db;
use schema public;
create database dataiku_test_db clone pc_dataiku_db;

-- 7.1.1.
use database dataiku_test_db;
use schema public;

-- 7.1.2
show tables like '%scored%';

-- 7.1.4
alter table "COVID19_TEST_SCORED_space-3a316aed-dku_node-df3ee930" rename to covid19_test_scored;

-- 7.1.5
drop table covid19_test_scored;

-- 7.1.6
select * from covid19_test_scored limit 10;

-- 7.1.7
undrop table covid19_test_scored;

-- 7.1.9
select * from covid19_test_scored limit 10;

-- 7.2.1
select province_state as "Location", count(*) as "count"
from covid19_test_scored
group by 1
order by 2 desc
limit 20;

-- 7.2.2
update covid19_test_scored set province_state = 'oops';

-- 7.2.3
select province_state as "Location", count(*) as "count"
from covid19_test_scored
group by 1
order by 2 desc
limit 20;

-- 7.2.9
select province_state as "Location",count(*) as "count" 
from covid19_test_scored 
before(statement => '01982883-0042-3ced-0000-01f1000463fe') 
group by 1 order by 2 desc limit 20;

-- 7.2.10
create or replace table covid19_test_scored_rewind clone covid19_test_scored 
before(statement => '01982883-0042-3ced-0000-01f1000463fe');

-- 7.2.11
select province_state  as "Location", count(*) as "Count"
from covid19_test_scored_rewind
group by 1
order by 2 desc
limit 20;

-- 7.2.12
 alter table covid19_test_scored_rewind swap with covid19_test_scored;
 
 -- 7.2.13
 select province_state  as "Location", count(*) as "Count"
from covid19_test_scored
group by 1
order by 2 desc
limit 20;

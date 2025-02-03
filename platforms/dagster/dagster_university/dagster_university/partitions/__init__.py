from dagster import MonthlyPartitionsDefinition, WeeklyPartitionsDefinition

from ..assets import constants

monthly_partition = MonthlyPartitionsDefinition(start_date=constants.START_DATE, end_date=constants.END_DATE)
weekly_partition = WeeklyPartitionsDefinition(start_date=constants.START_DATE, end_date=constants.END_DATE)

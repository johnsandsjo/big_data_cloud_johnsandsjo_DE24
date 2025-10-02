#imports
from pathlib import Path
import dlt
import dagster as dg
from dagster_dlt import DagsterDltResource, dlt_assets
from dagster_dbt import DbtCliResource, dbt_assets, DbtProject

#to import dlt script
import sys # just because we do not use packages
sys.path.insert(0, '../data_extract_load')
from load_job_ads import jobads_source

import os
DUCKDB_PATH = os.getenv("DUCKDB_PATH")
DBT_PROFILES_DIR = os.getenv("DBT_PROFILES_DIR")

#data warehouse
#db_path = str(Path(__file__).parents[1] / "data_warehouse/job_ads.duckdb")

#==========#
#dlt assets#
#==========#
#create dlt resource
dlt_resource = DagsterDltResource()

#create dlt asset
#need to collect dlt resource under dlt source
@dlt_assets(
    dlt_source = jobads_source(),
    dlt_pipeline = dlt.pipeline(
        pipeline_name = "job_search",
        dataset_name = "staging",
        destination = dlt.destinations.duckdb(DUCKDB_PATH)
    )
)
def dlt_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

#==========#
#dbt assets#
#==========#
#related paths for dbt projects
dbt_project_directory = Path(__file__).parents[1] / "data_transformation"
#profiles_dir = Path.home() / ".dbt"

#create dagster dbt project object
#dbt_project = DbtProject(project_dir=dbt_project_directory, 
#                         profiles_dir=profiles_dir)
dbt_project = DbtProject(project_dir=dbt_project_directory,
                         profiles_dir=Path(DBT_PROFILES_DIR))

dbt_resources = DbtCliResource(project_dir=dbt_project)

#create a manifest json file from dbt. Then Dagster uses this file
dbt_project.prepare_if_dev()

#create dagster dbt assets
@dbt_assets(manifest=dbt_project.manifest_path)
def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["test", "build"], context=context).stream()

#==========#
#Job#
#==========#
job_dlt = dg.define_asset_job(name= "job_dlt",
                              selection=dg.AssetSelection.keys("dlt_jobads_source_jobads_resource"))

job_dbt = dg.define_asset_job(name= "job_dbt",
                              selection=dg.AssetSelection.key_prefixes("warehouse", "marts"))
#==========#
#Schedule#
#==========#
schedule_dlt = dg.ScheduleDefinition(
    job=job_dlt, cron_schedule="58 11 * * *"
)

#==========#
#Sensor#
#==========#
@dg.asset_sensor(asset_key=dg.AssetKey("dlt_jobads_source_jobads_resource"),
                 job_name="job_dbt"
                 )
def dlt_load_sensor():
    yield dg.RunRequest()


#==========#
#Definitions#
#==========#
defs = dg.Definitions(assets=[dlt_load, dbt_models],
                      resources={"dlt" : dlt_resource,
                                 "dbt" : dbt_resources},
                        jobs = [job_dlt, job_dbt],
                        schedules=[schedule_dlt],
                        sensors=[dlt_load_sensor]
                      )
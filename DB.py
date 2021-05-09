from peewee import *
from playhouse.pool import *
from datetime import datetime, timedelta
import json
import traceback
from include.Logger import logging, get_logger
from playhouse.shortcuts import model_to_dict, dict_to_model
import os
import sys
log = get_logger(__name__)

from random import randint

import configparser
config = configparser.ConfigParser()
dir_name = os.path.basename(os.getcwd()).lower()
conf_file = f'{dir_name}.conf'
print(f'conf_file: {conf_file}')


if not os.path.isfile(conf_file):
    raise ValueError(f'CONFIG FILE NOT FOUND: {conf_file}')
config.read(conf_file)

db_name     = config['database']['db_name']
db_username = config['database']['db_username']
db_password = config['database']['db_password']
db_port     = config['database'].getint('db_port')


db = MySQLDatabase(db_name, user=db_username, passwd=db_password, port=db_port)
db.connect()


class BaseModel(Model):
    class Meta:
        database = db

class Record(BaseModel):
    R_ID       = PrimaryKeyField()
    Device_ID  = CharField(null=True)
    Firstname  = TextField(null=True)
    Lastname   = TextField(null=True)
    Gender     = TextField(null=True)
    Birthday   = TextField(null=True)
    Weight     = TextField(null=True)
    Height     = TextField(null=True)
    Keto_Level = TextField(null=True)
    # Start_Date = DateTimeField(null=True)
    # Test_Date  = DateTimeField(null=True)
    Start_Date = TextField(null=True)
    Test_Date  = TextField(null=True)
    Test_Time  = TextField(null=True)
    Remark     = TextField(null=True)



def initialize_database():
    ######################  Composulory to be run when initialize the Database #######################
    log.info(f'initialize_database')
    db.create_tables([Record])   # create tables in DB if not exist
    log.info(f"[Success] Tables created")


def create_record(data):
    log.info(f"DB.create_record: data - {data}")
    record = Record.create(Device_ID=data["device_id"],
                         Firstname=data["firstname"], 
                         Lastname=data["lastname"], 
                         Gender=data["gender"], 
                         Birthday=data["birthday"], 
                         Weight=data["weight"], 
                         Height=data["height"], 
                         Keto_Level=data["keto_level"], 
                         Start_Date=data["start_date"], 
                         Test_Date=data["test_date"], 
                         Test_Time=data["test_time"], 
                         Remark=data["remark"]
    )
    log.warning(f"record.R_ID: {record.R_ID}")


def get_records():
    log.info(f"DB.get_records")
    result = []
    query = Record.select()
    for i in query:
        item = {}
        item["record_id"] = i.R_ID
        item["device_id"] = i.Device_ID
        item["firstname"] = i.Firstname
        item["lastname"] = i.Lastname
        item["gender"] = i.Gender
        item["birthday"] = i.Birthday
        item["weight"] = i.Weight
        item["height"] = i.Height
        item["keto_level"] = i.Keto_Level
        item["start_date"] = i.Start_Date
        item["test_date"] = i.Test_Date
        item["test_time"] = i.Test_Time
        item["remark"] = i.Remark
        result.append(item)
    
    return result



if __name__=="__main__":
    pass

# CREATE DATABASE keto CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
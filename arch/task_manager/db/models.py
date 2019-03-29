#
#  Copyright 2019 The FATE Authors. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
from arch.api.utils import log_utils
from playhouse.pool import PooledMySQLDatabase
from arch.task_manager.settings import DATABASE
from peewee import Model, CharField, IntegerField, BigIntegerField, DateTimeField, TextField
import datetime

LOGGER = log_utils.getLogger()


data_base_config = DATABASE.copy()
# TODO: create instance according to the engine
engine = data_base_config.pop("engine")
db_name = data_base_config.pop("name")
DB = PooledMySQLDatabase(db_name, **data_base_config)


def close_db(db):
    try:
        if db:
            db.close()
    except Exception as e:
        LOGGER.exception(e)


class DataBaseModel(Model):
    class Meta:
        database = DB

    def to_json(self):
        return self.__dict__['__data__']

    def save(self, *args, **kwargs):
        if hasattr(self, "update_date"):
            self.update_date = datetime.datetime.now()
        super(DataBaseModel, self).save(*args, **kwargs)


class Job(DataBaseModel):
    job_id = CharField(max_length=50, primary_key=True)
    name = CharField(max_length=100, null=True, default='')
    task = CharField(max_length=50, index=True)
    module = CharField(max_length=50, null=True, index=True)
    scene_id = IntegerField(null=True, index=True)
    my_party_id = IntegerField(null=True, index=True)
    partner_party_id = IntegerField(null=True, index=True)
    my_role = CharField(max_length=10, null=True, index=True)
    config = TextField(null=True)
    status = CharField(max_length=50, null=True, default='ready')  # ready/running/success/failed/partial/deleted
    set_status = CharField(max_length=50, null=True)  # ready/running/success/failed/partial/deleted
    progress = IntegerField(null=True, default=0)
    current_step = CharField(max_length=100, null=True, index=True)
    create_date = DateTimeField(index=True)
    update_date = DateTimeField(index=True)
    begin_date = DateTimeField(null=True, index=True)
    end_date = DateTimeField(null=True, index=True)
    elapsed = BigIntegerField(null=True)

    class Meta:
        db_table = "job"

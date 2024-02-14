# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import re
import psycopg2


class JobfinderPipeline:
    def process_item(self, item, spider):
        return {key:self.remove_string_literals(value) for key,value in item.items()}
       
    def remove_string_literals(self,item):
        if isinstance(item,str):
            strip_item = item.strip()
            return re.sub(r"\s+"," ",item).strip()
        else:
            return item


class PostgresPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            host = 'host.docker.internal',
            port = '5432',
            database = 'jobs',
            user = 'spider',
            password = 'password'
        )
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        self.cursor.execute(
            '''
            INSERT INTO job_offers (
                position_id,
                position_name,
                searched_position,
                company,
                location,
                wage,
                portal,
                link
            ) VALUES(%s,%s,%s,%s,%s,NULLIF(%s,''),%s,%s) 
            ON CONFLICT (position_id) DO UPDATE SET
                location = EXCLUDED.location,
                wage = EXCLUDED.wage
            ''',
            (
                item.get("id"),
                item.get("position_name"),
                item.get("searched_position"),
                item.get("company"),
                item.get("location"),
                item.get("wage"),
                item.get("portal"),
                item.get("link"),
            )
        )
        self.conn.commit()

    def close_spider(self, spider):
        self.conn.close()



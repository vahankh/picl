import logging
import time
import json

from couchbase.bucket import Bucket
from couchbase.n1ql import N1QLQuery, CONSISTENCY_REQUEST
from couchbase.exceptions import CouchbaseError, KeyExistsError

from datetime import datetime

from core.picl import picl

class piclBucket(picl):
    _host = None
    _creds = None

    bucket_name = None
    _bucket_pass = None

    _cb = None

    retry_timeouts = [1, 5, 20, 60]  # in seconds

    def __init__(self, host, bucket_name, bucket_pass):

        self._host = host
        self.bucket_name = bucket_name
        self._bucket_pass = bucket_pass

        couch_bucket_url = 'couchbase://{0}/{1}'.format(host, bucket_name)

        self._cb = Bucket(couch_bucket_url, password=bucket_pass)
        self._cb.n1ql_timeout = 50000

    def save_document(self, key, doc):
        retry_i = 0
        while True:
            try:
                self._cb.upsert(key, doc)
                return True

            except CouchbaseError:
                logging.debug("--- key: {0}; data: {1} ---".format(key, json.dumps(doc)))
                logging.exception("--- Failed to execute upsert. ---")

                if retry_i < len(self.retry_timeouts):
                    logging.debug(
                        "--- Waiting for {0} seconds before trying again ---".format(self.retry_timeouts[retry_i]))
                    time.sleep(self.retry_timeouts[retry_i])
                    logging.debug("--- Trying one more time (attempt #{0}) ---".format(retry_i))
                else:
                    logging.info("--- Giving up on upsert ---")
                    return False

                retry_i += 1

    def n1ql_query(self, n1ql):
        retry_i = 0
        if not n1ql.endswith(";"):
            n1ql = n1ql + ";"

        n1qlObj = N1QLQuery(n1ql)
        # Not clear if we need that:
        # n1qlObj.consistency = CONSISTENCY_REQUEST

        n1qlObj.adhoc = False

        logging.info("Executing: " + n1ql);

        while True:
            try:
                result = self._cb.n1ql_query(n1qlObj)

                if not n1ql.upper().startswith("SELECT"):
                    result.execute()

                logging.info("--- Query executed successfully ---")
                return result

            except KeyboardInterrupt:
                raise
            except:
                logging.exception("--- Failed to execute query. ---")

                if retry_i < len(self.retry_timeouts):
                    logging.debug(
                        "--- Waiting for {0} seconds before trying again ---".format(self.retry_timeouts[retry_i]))
                    time.sleep(self.retry_timeouts[retry_i])
                    logging.debug("--- Trying one more time (attempt #{0}) ---".format(retry_i))
                else:
                    logging.info("--- Giving up on query ---")
                    return False
                retry_i += 1

    def update(self, id, dict):
        """id can be string in Couchbase"""
        set_str = ", ".join(["`{0}`='{1}'".format(col, val) for col, val in dict.items()])
        sql = "UPDATE `%s` SET %s WHERE meta().id='%s'" % (self.bucket_name, set_str, id)

        self.last_query = sql
        return self.n1ql_query(sql)

    def select(self, columns="*", joins=None, conditions=None, orderBy=None, groupBys=None, limit=1000, fetchAssoc=True):

        if self.bucket_name is None:
            return False

        if isinstance(columns, list):
            sql = "SELECT %s FROM `%s`" % (", ".join(columns), self.bucket_name)
        else:
            sql = "SELECT %s FROM `%s`" % (columns, self.bucket_name)

        if not joins is None:
            if isinstance(joins, list):
                sql += " " + " ".join(joins)
            else:
                sql += " " + joins

        if not conditions is None:
            sql += " WHERE "
            if isinstance(conditions, list):
                sql += " AND ".join(conditions)
            else:
                sql += conditions

        if not orderBy is None:
            sql += " ORDER BY "
            if isinstance(orderBy, list):
                sql += " ".join(orderBy)
            else:
                sql += " " + orderBy

        if not groupBys is None:
            sql += " GROUP BY "
            if isinstance(groupBys, list):
                sql += " ".join(groupBys)
            else:
                sql += " " + groupBys

        if not limit is None:
            sql += " LIMIT " + str(limit)

        self.last_query = sql

        result = self.n1ql_query(sql)

        if not result:
            return False
        
        if joins is None:
            return [i[self.bucket_name] for i in result]

        return result

    def remove_multi(self, keys):
        self._cb.remove_multi(keys, quiet=True)

    def upsert_multi(self, upsert_data):
        retry_i = 0

        logging.info("Upserting documents");

        if len(upsert_data) == 0:
            logging.info("multi_upsert of zero len. Exiting")
            return

        while True:
            try:
                self._cb.upsert_multi(upsert_data)

                logging.info("--- Query executed successfully ---")
                return True

            except KeyboardInterrupt:
                raise
            except:
                logging.exception("--- Failed to execute upsert_multi. ---")

                if retry_i < len(self.retry_timeouts):
                    logging.debug(
                        "--- Waiting for {0} seconds before trying again ---".format(self.retry_timeouts[retry_i]))
                    time.sleep(self.retry_timeouts[retry_i])
                    logging.debug("--- Trying one more time (attempt #{0}) ---".format(retry_i))
                else:
                    logging.info("--- Giving up on upsert_multi ---")
                    return False
                retry_i += 1


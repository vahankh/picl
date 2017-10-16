import datetime

from core.piclBucket import piclBucket

class Seed_Account(piclBucket):

    key_prefix = "acc-"

    def update_chunk(self, seeds):

        seeds_multi = {}
        for item in seeds:
            email = item['email']

            for key in list(item):
                value = item[key]
                if isinstance(value, datetime.date):
                    item[key] = value.strftime('%Y-%m-%d %H:%M:%S')
                    item['sync_ts'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            seeds_multi[self.key_prefix+email] = item

        return self.upsert_multi(seeds_multi)

    def update(self, id, dict):
        return super().update(self.key_prefix+id, dict)

    def remove_multi(self, keys):
        keys = [self.key_prefix+i for i in list(keys)]
        return super().remove_multi(keys)


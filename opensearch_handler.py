# builtins
import logging
import os
import datetime
import sys
# third party
from opensearchpy import OpenSearch
from opensearchpy.helpers import bulk

OPENSEARCH_HOST = os.environ.get("INPUT_OPENSEARCH_HOST")
OPENSEARCH_USERNAME = os.environ.get("INPUT_OPENSEARCH_USERNAME")
OPENSEARCH_PASSWORD = os.environ.get("INPUT_OPENSEARCH_PASSWORD")
OPENSEARCH_INDEX = os.environ.get("INPUT_OPENSEARCH_INDEX")

try:
    assert OPENSEARCH_HOST not in (None, '')
except:
    output = "The input OPENSEARCH_HOST is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert OPENSEARCH_USERNAME not in (None, '')
except:
    output = "The input OPENSEARCH_USERNAME is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert OPENSEARCH_PASSWORD not in (None, '')
except:
    output = "The input OPENSEARCH_PASSWORD is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    assert OPENSEARCH_INDEX not in (None, '')
    now = datetime.datetime.now()
    opensearch_index = f"{OPENSEARCH_INDEX}-{now.month}-{now.day}"
except:
    output = "The input OPENSEARCH_INDEX is not set"
    print(f"Error: {output}")
    sys.exit(-1)

try:
    es = OpenSearch(
        [OPENSEARCH_HOST],
        http_auth=(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        use_ssl=True,
        verify_certs=False,
        ssl_show_warn=False,
    )
except opensearch.exceptions.AuthorizationException as exc:
    output = "Authentication to opensearch failed"
    print(f"Error: {output}")
    sys.exit(-1)


class OpensearchHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        super(OpensearchHandler, self).__init__(*args, **kwargs)
        self.buffer = []

    def emit(self, record):
        try:
            record_dict = record.__dict__
            record_dict["@timestamp"] = int(record_dict.pop("created") * 1000)
            self.buffer.append({
                "_index": opensearch_index,
                **record_dict
            })
        except ValueError as e:
            output = f"Error inserting to Opensearch {str(e)}"
            print(f"Error: {output}")
            print(f"::set-output name=result::{output}")
            return

    def flush(self):
        # if the index is not exist, create it with mapping:
        if not es.indices.exists(index=opensearch_index):
            mapping = '''
            {  
              "mappings":{  
                  "properties": {
                    "@timestamp": {
                      "type":   "date",
                      "format": "epoch_millis"
                    }
                  }
                }
            }'''
            es.indices.create(index=opensearch_index, body=mapping)
        # commit the logs to opensearch
        bulk(
            client=es,
            actions=self.buffer
        )

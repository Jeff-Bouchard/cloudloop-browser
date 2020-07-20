

DEFAULT_LIMIT=10
DEFAULT_SCHEMA=[]

class RecordService():
    records = []
    limit = DEFAULT_LIMIT
    client = Airtable('appHcObTX28Vj70uM', 'Loops', api_key=os.environ['AIRTABLE_KEY'])
    record_schema = DEFAULT_SCHEMA
    def __init__(self, limit, schema):
        if limit:
            self.limit = limit
        if schema:
            self.schema = schema
        self.record_schema = schema
    def put_record(self, record):
        if self.record_schema.keys() == record.keys():
            self.records.append(record)
    def transmit_records(self):
        self.client.batch_insert(self.records)

app = Flask(__name__)
loop_rs = RecordService(10, {'link': '',
                             'channels': '',
                             'samples': '',
                             'sample_rate': '',
                             'bit_depth': ''})
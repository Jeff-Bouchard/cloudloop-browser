# cloudloop-flask

This is the CloudLoop SessionStore backend.
The goal is a reliable stateless web api layer sitting atop a redis-JSON Session Store.
Session updates are broadcast via https://socket.io

These models are implemented as raw JSON to ensure low overhead, with minimal transformations occuring in python.
We use a redis [rejson](https://oss.redislabs.com/redisjson/) instance with the Append-Only log enabled to achieve persitence and in-memory fast data access. Eventually, if we build a persistence layer on kafka, we could shut off the write-to-disk Append-Only-Log.

For this reason, there are two thin models: Session, and User.
User passwords are salted and hashed.
A session is a mutable description of a session in-progress. 
Loops are just HATEOAS references to external HTTPS URLs. No audio processing here!

### Running

build all the images with docker-compose build

run dev server with `./run.sh dev build && ./run.sh dev up`


The production configuration can be launched using `docker-compose up`.
All three containers run just fine on 1GB memory and 1 shared vCore. Could probably use ARM instances for the API and a "fat" redis

### Testing
The tests may be executed with `docker-compose -f docker-compose.tests.yml`
As the entire application is just a thin layer over redis, I consider these to be unittests and should only be run inside the containerized environment.

### Next Steps
- Reliably implement socket.io Acks so we fix the message retransmission issue.
- Send Loop Library records to Airtable or postgres in batch job. (redis Pub/sub)

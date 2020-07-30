from rejson import Client
import time
import os, sys
import subprocess

REDIS_HOST='redis'

rejson_client = Client(host=REDIS_HOST,
                      port=6379,
                      decode_responses=True,
                      db=1)

redis_healthy = False

saved_args=sys.argv[1:]
print(f'Subprocess command: {saved_args}')

while not redis_healthy:
    try:
        res = rejson_client.ping()
        print(f'Redis healthy? {res}')
        if res == True:
            redis_healthy = True
            print(f'Redis is up. Running python.')
            subprocess.run(saved_args)
            exit(0)
    except Exception as e:
        print(f'rejson not ready: {str(e)}')
        time.sleep(1)

from datetime import datetime,date,time,timedelta
import asyncio
import time

lol = {}

if __name__ == "__main__":
    lol['noob'] = {'lol':datetime.now()}
    now = datetime.now()
    z = lol['noob']['lol']-now
    y = z.total_seconds()
    #y = timedelta(z)
    print(y)

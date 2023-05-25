from read_configuration import Configuration
from messaging_api import MessagingAPI
from suspended_queue import execute
import threading
import asyncio
import time

class MainClass:
    config_data = None
    polling_started = set()

    def __init__(self):
        self.config_data = Configuration.get_instance().read_file()
        
    def start(self):
        while True:
            self.process()
            time.sleep(30)
            print("----------------------------------------------------------\n")
        
    def process(self):
        
        for row in self.config_data:
            app = row[0]
            app_url = row[1]
            mq_id = row[2]
            pattern = "{}-{}".format(app,mq_id)
            is_suspended = asyncio.run(MessagingAPI(app, app_url).is_suspended(mq_id))
            has_polling_started = (pattern in self.polling_started)
            if(is_suspended):
                if(not has_polling_started):
                    dependancy_urls = row[4].split(",")
                    thread = threading.Thread(target=execute, args=(app, app_url, mq_id, list(dependancy_urls)))
                    thread.start()
                    self.polling_started.add(pattern)
                else:
                    print("{} - MQ:{} is suspended and polling is in progress".format(app, mq_id))
            else:
                if(has_polling_started):
                    self.polling_started.discard(pattern)
            print("MQ {}:{} --> Is Suspended: {} | Polling Started : {}".format(app, mq_id, is_suspended, has_polling_started))        



MainClass().start()
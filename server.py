import time
from enum import Enum
from multiprocessing import Process
import servepy

def sample_func():
    i = 1
    while(True):
        print(f'HERE {i}')
        i += 1
        time.sleep(1) # wait 1 second

class Handler:
    def __init__(self):
        self.pm = ProcessManager()

    def get(self, request, response):
        response.set('Content-Type', 'application/json')
        response.status(200)

        status = self.pm.status
        return response.json({ 'System': 'online', 'Status': status })

    def stop(self, request, response):
        stopped = self.pm.stop()
        response.set('Content-Type', 'application/json')
        response.status(200)

        status = self.pm.status
        return response.json({ "Success": stopped, "Status": status})

    def start(self, request, response):
        started = self.pm.start()
        response.set('Content-Type', 'application/json')
        response.status(200)

        status = self.pm.status
        return response.json({ "Success": started, "Status": status})

class ProcessManagerStatus(str, Enum):
    IDLE='IDLE'
    STARTING='STARTING'
    RUNNING='RUNNING'
    STOPPING='STOPPING'

class ProcessManager:
    def __init__(self):
        self.ps = None
        self.status = ProcessManagerStatus.IDLE

    def start(self, **kwargs):
        # stop running process if needed
        if self.status == ProcessManagerStatus.RUNNING:
            stopped = self.stop()

            if not stopped:
                return False

        # set idle for a quick moment
        self.status = ProcessManagerStatus.IDLE
        
        # create the new process
        self.ps = Process(target=sample_func)
        self.status = ProcessManagerStatus.STARTING

        self.ps.start()
        self.status = ProcessManagerStatus.RUNNING

        return True

    def stop(self):
        # if no running process do nothing
        if self.status != ProcessManagerStatus.RUNNING:
            return False

        # set stopping for a quick moment
        self.status = ProcessManagerStatus.STOPPING
        self.ps.kill()

        self.status = ProcessManagerStatus.IDLE
        return True



app = servepy.App()
router = servepy.Router()

handler = Handler()
router.get('/', handler.get)
router.get('/stop', handler.stop)
router.get('/start', handler.start)

app.use(router)

hostname = '10.88.111.31'
port = 80

def callback():
    print(f'Server running at {hostname}:{port}')

app.listen(port=port, hostname=hostname, callback=callback)

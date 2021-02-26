import sys
import time

from util.logger import setup_logging

from multiprocessing import Process
from multiprocessing import active_children

import flask

app = flask.Flask(__name__)

logger = setup_logging()
STATE = 2

@app.route("/spawn", methods=["GET"])
def processor():
    spawn()
    return "Spawned!\n"

@app.route("/init", methods=["GET"])
def init():
    monitor(STATE)

def monitor(state: int):
    """Check current state of system"""
    while True:
        if len(active_children()) < state:
            logger.awaiting(
                "awaiting reconciliation system state: %d with desired state: %d" % (len(active_children()), state)
            )
        elif len(active_children()) == state:
            logger.stable("STABLE: number of processes: %d" % (state))

        pids = ", ".join([str(obj.pid) for obj in active_children()])
        logger.info(
            "INFO: current PIDs: %s" % (pids)
        )
        time.sleep(1)

def spawn():
    """Spawn new processes"""
    proc_obj = Process(target=do_some_processing)
    logger.info("INFO: process spawned")
    proc_obj.start()

def do_some_processing():
    """Dummy processing function"""
    while True:
        pass

if __name__ == '__main__':
    STATE = int(sys.argv[1])
    app.run(port=8080)

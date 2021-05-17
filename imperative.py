import sys
import time

from util.logger import setup_logging

from multiprocessing import Process
from multiprocessing import active_children

import flask

app = flask.Flask(__name__)

logger = setup_logging()
STATE = 2

def get_state():
    return len(active_children())

@app.route("/spawn", methods=["GET"])
def processor():
    spawn()
    return "Spawned!\n"

@app.route("/init", methods=["GET"])
def init():
    kubey(STATE)

def kubey(state):
    monitor(state)

def monitor(state: int):
    """Check current state of system"""
    while True:
        if get_state() < state:
            logger.awaiting(
                "awaiting reconciliation system state: %d with desired state: %d" % (get_state(), state)
            )
        elif get_state() == state:
            logger.stable("number of processes: %d" % (state))

        pids = ", ".join([str(obj.pid) for obj in active_children()])
        logger.info(
            "current PIDs: %s" % (pids)
        )
        time.sleep(1)

def spawn():
    """Spawn new processes"""
    proc_obj = Process(target=do_some_processing)
    logger.info("process spawned")
    proc_obj.start()

def do_some_processing():
    """Dummy processing function"""
    while True:
        pass

if __name__ == '__main__':
    try:
        STATE = int(sys.argv[1])
    except:
        print("Usage: python imperative.py <num. of processes>")
        sys.exit(0)
    app.run(port=8080)

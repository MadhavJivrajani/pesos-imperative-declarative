import sys
import time

from util.logger import setup_logging

from multiprocessing import Process
from multiprocessing import active_children

logger = setup_logging()

def get_state():
    return len(active_children())

def processor(command):
    """Execute a command provided by the controller"""
    command()

def monitor(state: int):
    """Monitor the current state of the system
    and issue appropriate commands to the processor
    to reconcile current state with reconciled state.
    """
    if get_state() < state:
        logger.reconcile(
            "attempting reconciling system state: %d with desired state: %d" % (get_state(), state)
        )
        processor(spawn)
    elif get_state() == state:
        logger.stable("number of processes: %d" % (state))

def spawn():
    """Spawn new processes"""
    proc_obj = Process(target=do_some_processing)
    logger.info("process spawned")
    proc_obj.start()

def do_some_processing():
    """Dummy processing function"""
    while True:
        pass

def controller(state: int):
    """Monitors state of the current system and takes
    appropriate actions to reconcile current state with
    the desired state.
    """

    # control loop
    while True:
        monitor(state)
        pids = ", ".join([str(obj.pid) for obj in active_children()])
        logger.info(
            "current PIDs: %s" % (pids)
        )
        time.sleep(1)
        
def kubey(state: int):
    controller(state)

if __name__ == '__main__':
    try:
        state = int(sys.argv[1])
    except:
        print("Usage: python declarative.py <num. of processes>")
        sys.exit(0)
    kubey(state)

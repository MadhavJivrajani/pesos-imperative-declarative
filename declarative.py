import sys
import time

from util.logger import setup_logging

from multiprocessing import Process
from multiprocessing import active_children

logger = setup_logging()

def processor(command):
    """Execute a command provided by the controller"""
    command()

def monitor(state: int):
    """Monitor the current state of the system
    and issue appropriate commands to the processor
    to reconcile current state with reconciled state.
    """
    if len(active_children()) < state:
        logger.reconcile(
            "attempting reconciling system state: %d with desired state: %d" % (len(active_children()), state)
        )
        processor(spawn)
    elif len(active_children()) == state:
        logger.stable("STABLE: number of processes: %d" % (state))

def spawn():
    """Spawn new processes"""
    proc_obj = Process(target=do_some_processing)
    logger.info("INFO: process spawned")
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
            "INFO: current PIDs: %s" % (pids)
        )
        time.sleep(1)
        
def main(state: int):
    controller(state)

if __name__ == '__main__':
    state = int(sys.argv[1])
    main(state)

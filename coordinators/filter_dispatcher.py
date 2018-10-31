import sys
from os import path

sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

from middleware.connection import SuscriberSocket, DispatcherSocket, ReplicationSocket
from operations.filter import Filter
import middleware.constants as const

class DataFilterReplicator(object):

    def __init__(self, port, dispatchport, pattern):
        
        self.socket = SuscriberSocket(port,
                [const.NEW_DATA, const.END_DATA])
        
        self.dispatchsocket = DispatcherSocket(dispatchport)

        self.signalsocket = ReplicationSocket(7777)

        self.filter = Filter(pattern)

    def _parse_data(self, msg):

        # Split the id from the row
        mid, row = msg.split(" ", 1)

        if (mid == const.END_DATA):
            return mid, ""

        row = row.split('\n')
        
        # Becuase the last element is an empty
        # string becuase of the splitter 
        row.pop()

        d = {}

        for item in row:
            k, v = item.split('=')
            d[k] = v

        return mid, d

    def _recv_data(self):

        msg = self.socket.recv()

        return self._parse_data(msg)

    def _send_data(self, row):

        msg = ""

        # Convert the row (dictionary) into
        # a string to send
        items = list(row.items())
        
        for it in items:
            msg += it[0] + '=' + it[1] + '\n'

        print(msg)
        self.dispatchsocket.send(msg)

    def run(self):
 
        print("Filter replicator started")

        mid, row = self._recv_data()

        while (int(mid) == const.NEW_DATA):

            if self.filter.filter(row):
                self._send_data(row)

            mid, row = self._recv_data()

        self.signalsocket.send("{tid} {data}".format(tid=const.END_DATA, data="END_DATA"))
    
        input("Enter to finish")

        print("Filter replicator finished")


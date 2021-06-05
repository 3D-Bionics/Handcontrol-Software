from pySerialTransfer import pySerialTransfer as transfer
from hand_object import hand
import time

class Comframe:
    
    def __init__(self, port, hand: hand):

        self._hand = hand

        try:
            # Create Link
            self._link = transfer.SerialTransfer(port)

            # Set Callbacks for automatic receiving and processing of packages
            self._callbacklist = [self._receivePos, self._receiveDebug]
            self._link.set_callbacks(self._callbacklist)

            # Open Link
            self._link.open()


        except KeyboardInterrupt:
            try:
                self._link.close()
            except:
                pass

        except:
            import traceback
            traceback.print_exc()
            quit()
    
    def __del__(self):
        try:
            self._link.close()
        except:
            pass

    # Method for extending support for optional handtracker on seperate serial Port
    def attachHandTracker(self, port):
        pass

    
    # Callback for receiving position update packages (package id 0)
    def _receivePos(self):
        buffer = self._link.rx_obj(obj_type=list,obj_byte_size=20,list_format='i')

        self._hand.setPos(buffer)

    # Callback for debug purposes (package id 1) [NOT YET IMPLEMENTED]
    def _receiveDebug(self):
        pass

    # Send specific position to the arduino
    def sendPosList(self, positions: list[int]):
        if hand.checkPos(positions):
            self._link.send(self._link.tx_obj(positions))

    # Send position of hand to arduino
    def sendPos(self):
        self._link.send(self._link.tx_obj(self._hand.getPos()))

    # process all incoming packages
    def processAll(self):
        while(self._link.tick()):
            pass
    
    # process one incoming package
    def processOne(self):
        self._link.tick()

    
    @staticmethod
    def getOpenPorts() -> list:
        return transfer.open_ports()
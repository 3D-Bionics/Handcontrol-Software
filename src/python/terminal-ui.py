import npyscreen
import curses.ascii
from hand_object import hand
from communication_framework import Comframe 
from ui_widgets import TSlider, BoxSelectOne, BoxOptions

class MainForm(npyscreen.FormBaseNew):
    def __init__(self,*args,**keywords):
        super(MainForm,self).__init__(name="3D-Bionics Hand Controll Software",lines=22,*args,**keywords)

        self.Hand = self.parentApp.Hand
        self.Comframe = self.parentApp.Comframe

    def create(self):
        y, x = self.useable_space()

        left = round(x*2/3)
        
        # Create UI

        #self.nextrely = round(y/2)-5
        self.nextrely = 3
        self.klein = self.add(TSlider, max_width=left,name = "Klein")
        self.nextrely +=1
        self.ring = self.add(TSlider, max_width=left, name = "Ring")
        self.nextrely +=1
        self.mittel = self.add(TSlider, max_width=left,  name = "Mittel")
        self.nextrely +=1
        self.zeige = self.add(TSlider, max_width=left, name = "Zeige")
        self.nextrely +=1
        self.daumen = self.add(TSlider, max_width=left, name = "Daumen")

        self.nextrely = 2
        self.quickPos = self.add(BoxSelectOne, relx = left + 10, max_height= round((y-2)/2), name = "Quick Positions")
        self.nextrely += 2
        self.button_loop = self.add(BoxOptions, relx= left +10)

        # init handlers

        handlers = {
            '^Q': self.exit_func,
            curses.ascii.ESC: self.exit_func
        }

        self.add_handlers(handlers)

        # Additional Config

        self.keypress_timeout=1

    def afterEditing(self):
        self.parentApp.setNextForm(None)

    def while_waiting(self):
        self.Comframe.processQueue()
        self.updatePos()


    def sendPos(self):
        
        new_pos = [[
            int(self.klein.value),
            int(self.ring.value),
            int(self.mittel.value),
            int(self.zeige.value),
            int(self.daumen.value)
            ]]

        self.Comframe.queue_clear()
        self.Comframe.queue_position(new_pos)
        

     

    def updatePos(self):
        self.klein.set_value(self.Hand.getKlein())
        self.mittel.set_value(self.Hand.getMittel())
        self.ring.set_value(self.Hand.getRing())
        self.zeige.set_value(self.Hand.getZeige())
        self.daumen.set_value(self.Hand.getDaumen())
        self.display()
    
    # Various functions
    def exit_func(self, _input):
        exit(0)


class hand_controll(npyscreen.NPSAppManaged):
    def onStart(self):
        self.Hand = hand([0,0,0,0,0])
        self.Comframe = Comframe('/dev/ttyUSB0',self.Hand)
        self.addForm("MAIN", MainForm)

    
if __name__ == "__main__":
    
    App = hand_controll()
    App.run()
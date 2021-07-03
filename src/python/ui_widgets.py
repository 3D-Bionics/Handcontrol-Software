import npyscreen

from hand_object import hand
from positions import hand_positions


# Sliders for displaying current position of hand
class Slider(npyscreen.SliderPercent):
    def __init__(self,screen,block_color='CAUTIONHL',*args,**keywords):
        super(Slider,self).__init__(screen,out_of=100, step=5, editable= False, block_color=block_color ,*args,**keywords)

    def when_value_edited(self):
        self.parent.sendPos()

class TSlider(npyscreen.TitleText):
    _entry_type=Slider

# Slider for ajusting delay between position changes
class _TimeSlider(npyscreen.Slider):
    def __init__(self,screen,block_color='VERYGOOD',*args,**keywords):
        super(_TimeSlider,self).__init__(screen,lowest = 0.01, out_of=1, step=0.01, editable= True, block_color=block_color ,*args,**keywords)
    
    def when_value_edited(self):
        self.value = round(self.value,2)
        self.find_parent_app().comframe.delay = self.value

    def translate_value(self):
        stri = "%ss / %ss" %(self.value, self.out_of)
        if isinstance(stri, bytes):
            stri = stri.decode(self.encoding, 'replace')
        l = (len(str(self.out_of)))*2+6
        stri = stri.rjust(l)
        return stri

class TimeSlider(npyscreen.TitleText):
    _entry_type=_TimeSlider

# Widget for selecting pre-programmed hand positions
# Positions are located in file positions.py
class SelectOne(npyscreen.SelectOne):
    def __init__(self,screen,*args,**keywords):
        super(SelectOne,self).__init__(screen,values=list(hand_positions.keys()),value=0,*args,**keywords)

    def setPosition(self):
        options = self.get_selected_objects()
        self.find_parent_app().comframe.queue_clear()
        for option in options:
            self.find_parent_app().comframe.queue_position(hand_positions[option])

    def when_value_edited(self):
        self.setPosition()

class BoxSelectOne(npyscreen.BoxTitle):
    _contained_widget = SelectOne


# Widget for selecting various options
class Options(npyscreen.MultiSelect):

    def __init__(self,screen,*args,**keywords):
        super(Options,self).__init__(screen,values=['Loop','Pause','Manual','Custom Delay'],*args,**keywords)

    def when_value_edited(self):
        options = self.get_selected_objects() or []
        comframe = self.find_parent_app().comframe

        if 'Loop' in options:
            comframe.loop = True
        else:
            comframe.loop = False

        if 'Pause' in options:
            comframe.pause = True
        else:
            comframe.pause = False
        
        if 'Manual' in options:
            self.parent.klein.editable = True
            self.parent.ring.editable = True
            self.parent.mittel.editable = True
            self.parent.zeige.editable = True
            self.parent.daumen.editable = True
        else:
            self.parent.klein.editable = False
            self.parent.ring.editable = False
            self.parent.mittel.editable = False
            self.parent.zeige.editable = False
            self.parent.daumen.editable = False

        if 'Custom Delay' in options:
            self.parent.timeslider.hidden = False
        else:
            self.parent.timeslider.hidden = True

class BoxOptions(npyscreen.BoxTitle):
    _contained_widget = Options
    name = 'Options'

from npyscreen import fmPopup, wgmultiline 
from communication_framework import getOpenPorts

class _PortBox(npyscreen.ComboBox):

    def h_change_value(self, input):
        self.values = getOpenPorts()
        self.find_parent_app().comframe.reconnect()
        "Pop up a window in which to select the values for the field"
        F = fmPopup.Popup(name = self.name)
        l = F.add(wgmultiline.MultiLine, 
            values = [self.display_value(x) for x in self.values],
            return_exit=True, select_exit=True,
            value=self.value)
        F.display()
        l.edit()
        self.value = l.value

    def when_value_edited(self):
        comframe = self.find_parent_app().comframe        
        try:
            comframe.reconnect(self.values[self.value])
        except:
            comframe.reconnect()


class PortBox(npyscreen.TitleCombo):
    _entry_type=_PortBox

    def __init__(self,screen,*args,**keywords):
        super(PortBox,self).__init__(screen,name = "Serial Port:", use_two_lines=False, *args,**keywords)

        currentPort = self.find_parent_app().comframe.port
        self.values.append(currentPort)
        self.value = self.values.index(currentPort)

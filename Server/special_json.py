import datetime
from jsonschema import validate


class CON:
    AUT = "AUT" #authorization
    PSH = "PSH" #client sands message
    CHK = "CHK" #check updates 
    UPD = "UPD" #request for update

    DEN = "DEN" #denay of servise
    ACK = "ACK" #acknowledgement
    APP = "APP" #last message id
    PLL = "PLL" #get new messages

    DFT = "DFT" #default


js_template = {
    'Cond'  : 'string',
    'Name'  : 'string',
    'Index' : 'int',
    'Time'  : 'string',
    'Data'  : 'string',
}


class js_message:

    def __init__(
            self,
            cond = CON.DFT,
            index = 0,
            name = "Username",
            time = datetime.datetime.now().strftime('%H:%M'),
            data = ""):
        
        self.Cond   = cond
        self.Name   = name
        self.Index  = index
        self.Time   = time
        self.Data   = data


    def copy(
            self):
        
        new_mes = js_message(self.Cond, self.Name, self.Index, self.Time, self.Data)
        
        return new_mes


    def from_js(
            self,
            json_obj,):
            
        try:
            if  all(i in json_obj
            for i in ['Cond', 'Name', 'Time', 'Index', 'Data']):

                self.Cond   = json_obj['Cond']
                self.Name   = json_obj['Name']
                self.Time   = json_obj['Time']
                self.Index  = json_obj['Index']
                self.Data   = json_obj['Data']

                return 1
        
        except Exception:
            return 0


    def to_js(self):
        return {
            "Cond"  : self.Cond,
            "Name"  : self.Name,
            "Time"  : self.Time,
            "Index" : self.Index,
            "Data"  : self.Data,
        }

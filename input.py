import curlparser, json
import pandas as pd

class TestCase:
    def __init__(self, cUrl):
        self.tcs = list()
        self.cUrl = cUrl
        parser = curlparser.parse(self.cUrl)
        self.hdict = parser.header
        self.bodyreq = parser.data
        self.bdict = json.loads(parser.data)
        self.count = 0
        self.keylist = []

    def main(self):
        self.headertc(self.hdict)
        self.iterdict(self.bdict)
        self.bodytc(self.keylist)
        
    def headertc(self, hdict):
        #Header null test cases:
        for k,v in hdict.items():
            self.count += 1
            tProcedure = [f"{x}:{y}" for x,y in self.hdict.items() if x!=k]
            tP = ''
            for i in tProcedure:
                tP += i + " \n"
            tP += f"{k} : null"
            tc = (self.count,"Validation","Null Headers","Disable "+k,
                " ", tP, " ", " ", " ", " ", " ")
            self.tcs.append(tc)

        #Headers empty test cases
        for k,v in self.hdict.items():
            self.count +=1
            tProcedure = [f"{x}:{y}" for x,y in self.hdict.items() if x!=k]
            tP = ''
            for i in tProcedure:
                tP += i + " \n"
            tP += f"{k} : ''"
            tc = (self.count, "Validation","Empty Headers","Empty value for "+k,
                " ",tP, " ", " ", " ", " " ," ")
            self.tcs.append(tc)
    
    def getkey(self,name):
        return self.keylist.append(name)

    def iterdict(self,d):
        if isinstance(d, dict):
            for k,v in d.items():        
                if isinstance(v, dict):
                    self.iterdict(v)
                elif isinstance(v,list):
                    for i in v:
                        if isinstance(i,dict):
                            self.iterdict(i)
                        else:
                            self.getkey(k)
                else:            
                    self.getkey(k)

    def bodytc(self,keylist):
        for i in keylist:
            self.count +=1
            tc = (self.count,"Validation","Empty Body values",i + " : empty",
                  " ","Empty value for "+i+"\nLeave others keys values as default",
                  self.bodyreq," "," "," "," ")
            self.tcs.append(tc)

        for i in keylist:
            self.count +=1
            tc = (self.count,"Validation","Empty Body values",i + " : empty",
                  " ","Empty value for "+i+"\nLeave others keys values as default",
                  self.bodyreq, " "," "," "," ")
            self.tcs.append(tc)


fd = open("curl.txt","r")
cUrl = """"""
for lines in fd:
    lines = lines.rstrip()
    cUrl += lines + "\n"
testcase = TestCase(cUrl)
testcase.main()

tcases = testcase.tcs
df = pd.DataFrame(tcases, columns=['Id','Group Name','Sub Group Name',
'Test Case Description','Precondition','Test Case Procedure',
'Test data','Expected Output','Result','Test date','Note'])
df.to_excel('testcases.xlsx',sheet_name='test')
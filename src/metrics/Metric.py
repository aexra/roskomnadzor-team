class Metric:
    count = 0
    
    def __init__(self, name: str, desc: str, result: str, recs: str, lvl: 0|1|2):
        
        self.oid = Metric.count
        self.name = name
        self.desc = desc
        self.result = result
        self.recs = recs
        self.lvl = lvl
        
        Metric.count += 1

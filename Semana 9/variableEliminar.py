class BayesianNetwork:
    
    def __init__(self):
        nodes = {}
    
    def getOrder(self):
        return [
                {"node":"L", "parents":["G"],      "probabilities":[{"condition":{"G":100, "L":100}, "value":0.9},
                                                                    {"condition":{"G":100, "L":0}, "value":0.1},
                                                                    {"condition":{"G":0, "L":100}, "value":0.6},
                                                                    {"condition":{"G":0, "L":0}, "value":0.4},
                                                                    {"condition":{"G":50, "L":100}, "value":0.01},
                                                                    {"condition":{"G":50, "L":0}, "value":0.99}]},

                {"node":"G", "parents":["D", "I"], "probabilities":[{"condition":{"G":100, "I":100, "D":100}, "value":0.5},
                                                                    {"condition":{"G":100, "I":100, "D":0}, "value":0.9},
                                                                    {"condition":{"G":100, "I":0, "D":100}, "value":0.05},
                                                                    {"condition":{"G":100, "I":0, "D":0}, "value":0.3},
                                                                    {"condition":{"G":0, "I":100, "D":100}, "value":0.3},
                                                                    {"condition":{"G":0, "I":100, "D":0}, "value":0.08},
                                                                    {"condition":{"G":0, "I":0, "D":100}, "value":0.25},
                                                                    {"condition":{"G":0, "I":0, "D":0}, "value":0.3},
                                                                    {"condition":{"G":50, "I":100, "D":100}, "value":0.2},
                                                                    {"condition":{"G":50, "I":100, "D":0}, "value":0.02},
                                                                    {"condition":{"G":50, "I":0, "D":100}, "value":0.7},
                                                                    {"condition":{"G":50, "I":0, "D":0}, "value":0.3}]},

                {"node":"S", "parents":["I"],      "probabilities":[{"condition":{"I":100,"S":100}, "value":0.8},
                                                                    {"condition":{"I":100,"S":0}, "value":0.2},
                                                                    {"condition":{"I":0,"S":100}, "value":0.05},
                                                                    {"condition":{"I":0,"S":0}, "value":0.95}]}, 

                {"node":"I", "parents":[],         "probabilities":[{"condition":{"I":100}, "value":0.3},
                                                                    {"condition":{"I":0}, "value":0.7}]},

                {"node":"D", "parents":[],         "probabilities":[{"condition":{"D":100}, "value":0.4},
                                                                    {"condition":{"D":0}, "value":0.6}]}, 
               ]

def join(factor1, factor2):
    newVars = list(factor1["variable"])
    newVars.extend([element for element in factor2["variable"] if element not in newVars])

    newP = []
    #print("JOin vars: " + str(newVars) + " allcomb: " + str(getAllConditions(newVars)))
    #print("factor1: " + str(factor1))
    #print("factor2: " + str(factor2))
    for cond in getAllConditions(newVars):
        prob = 1.0

        for c in factor2["p"]:
            #print("cond: " + str(cond) +" c: "+str(c["condition"])+" bool: " + str(contains(cond, c["condition"])))
            if contains(cond, c["condition"]):
                #print("mult: " + str(prob) + " c: " + str(c["value"]))
                prob *= c["value"]

        for c in factor1["p"]:
            #print("cond: " + str(cond) +" c: "+str(c["condition"])+" bool: " + str(contains(cond, c["condition"])))
            if contains(cond, c["condition"]):
                #print("mult: " + str(prob) + " c: " + str(c["value"]))
                prob *= c["value"]

        newP.append({'value': prob, 'condition': cond})

    #print("res Join: " + str({"variable": newVars, "p": newP}))
    return {"variable": newVars, "p": newP}

def contains(cond, c):
    for key in c:
        if key in cond:
            if cond[key] != c[key]:
                return False
        else:
            return False
    return True

def getAllConditions(vars):
    pl = {
        "D":[100, 0],"I":[100, 0], "S":[100, 0], "G":[100, 50, 0], "L": [100, 0]
    }
    comb = []
    
    for v in vars:
        if len(comb) == 0:
            for t in pl[v]:
                comb.append({v:t})
        else:
            tmp = []
            for cm in comb:
                for t in pl[v]:
                    r = {v:t}
                    r.update(dict(cm))
                    tmp.append(r)
            comb = tmp
    return comb

def containsElim(old, cond):
    for key in cond["condition"]:
        if key in old["condition"]:
            if old["condition"][key] != cond["condition"][key]:
                return False
        else:
            return False
    return True

def eliminateSum(factor, oldCond, var):
    newP = []
    #print("Varaible eliminar: " + str(var))
    #print("vars: " + str(factor["variable"]))
    factor["variable"].remove(var)
    #print("Variable allconditions: " + str(getAllConditions(factor["variable"])))
    for cond in getAllConditions(factor["variable"]):
        newP.append({"condition": cond, "value":0.0})
    
    for cond in newP:
        for old in oldCond:
            #print("COnd: " +str(cond) +" oldC: " + str(old) + " res: " + str(containsElim(old, cond)))
            if containsElim(old, cond):
                cond["value"] = cond["value"] + old["value"]

    #print( "newP: "+ str( newP))
    return newP

def addFactor(v, evidence):

    factor = {"variable": list(v["parents"]), "p": v["probabilities"]}
    factor["variable"].append(v["node"])
    #print("probabilidades: " + str(factor["p"]))
    #print("evidence EV: " + str(evidence))
    for e in evidence:
        #print("Condition Ev: " + str (e in factor["variable"]))
        if e in factor["variable"]:
            newP = []
            for c in factor["p"]:
                #print("condition: " + str(c) + " event: "+ str(e) )
                for cond in c["condition"]:
                    #print ("boll: " + str(cond == e and c["condition"][cond] == evidence[e]))
                    if cond == e and c["condition"][cond] == evidence[e]:
                        newP.append(c)
                        break
            factor["p"] = newP
            #print("1 ******")
            factor["p"] = eliminateSum(factor, factor["p"], e)
            #print("Super factor" + str(factor))
            #print("2 ******")
    #print("factors: " + str(factor))
    return factor

def ask(target, evidence):
    network = BayesianNetwork()
    
    topologicalOrder = network.getOrder()
    #print(topologicalOrder)
    factors = []

    for v in topologicalOrder:

        factors.append(addFactor(v, evidence))
        #print("v: " + str(v["node"]))
        #print("Factors: " + str(factors))
        #print(" ")
        #print(target["node"])
        #print(not(v in evidence))
        #print(target["node"] != v)
        if target["node"] != v["node"] and not(v["node"] in evidence):
            temp = factors[0]
            #print("Temp: " + str(temp))
            #print("Size: " + str(len(factors)))
            for fact in factors[1:]:
                temp = join(temp, fact)
            #print("Temp after: " + str(temp))
            #print("Factors if: " + str(factors))
            #print(" ")
            #factor["p"] = eliminateSum(factor, factor["p"], e)
            temp["p"] = eliminateSum(temp, temp["p"], v["node"])
            #eliminate(v, temp)
            #print("Factors elim: " + str(factors))
            #print(" ")
            factors = []
            factors.append(temp)
        #print("---------------")
    #print ("Factors end: "+str(factors))
    #print(" ")

    result = factors[0]
    for fact in factors[1:]:
        result = join(result, fact)
    
    #print ("Result end: "+str(result))
    #print(" ")

    for ans in result["p"]:
        if target["node"] in ans["condition"]:
            if  target["value"] == ans["condition"][target["node"]]:
                return ans["value"]
    return "-1"
    
res = ask({"node":"D","value":0}, {"G":100})

print("Main Resp: " + str(res))


class Formula:
    formula1 = None
    formula2 = None
    
    def __init__(self):
        raise NotImplementedError
    
    def __repr__(self):
        return str(self.formula1)
    
    def evaluate(self, variables):
        raise NotImplementedError

class Conjunction(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2
    
    def __repr__(self):
        return "({}∧{})".format(str(self.formula1), str(self.formula2))
    
    def evaluate(self, variables):
        return (min(self.formula1.evaluate(variables)[0], self.formula2.evaluate(variables)[0]), [])

class Disjunction(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __repr__(self):
        return "({}∨{})".format(str(self.formula1), str(self.formula2))

    def evaluate(self, variables):
        return (max(self.formula1.evaluate(variables)[0], self.formula2.evaluate(variables)[0]), [])

class Implication(Formula):
    def __init__(self, formula1, formula2):
        self.formula1 = formula1
        self.formula2 = formula2

    def __repr__(self):
        return "({}→{})".format(str(self.formula1), str(self.formula2))
        
    def evaluate(self, variables):
        return (max(1 - self.formula1.evaluate(variables)[0], self.formula2.evaluate(variables)[0]), [])

class Negation(Formula):
    def __init__(self, formula):
        self.formula1 = formula
    
    def __repr__(self):
        return "¬{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        return (1 - self.formula1.evaluate(variables), [])

class Variable(Formula):
    def __init__(self, variable):
        self.formula1 = variable
    
    def evaluate(self, variables):
        return (variables[self.formula1], [])

class Static(Formula):
    def __init__(self, value):
        self.formula1 = value
    
    def evaluate(self, variables):
        return (self.formula1, [])

class Always(Formula):
    def __init__(self, formula, accumulated_result = 1):
        self.formula1 = formula
        self.accumulated_result = accumulated_result
    
    def __repr__(self):
        return "G{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        result = min(self.accumulated_result, self.formula1.evaluate(variables)[0])
        return (result, [Always(self.formula1, result)])

def eta(n):
    return max(1 / (n + 1), 0)

class AlmostAlways(Formula):
    def __init__(self, formula, accumulated_result = 1, avoided_number = 0):
        self.formula1 = formula
        self.accumulated_result = accumulated_result
        self.avoided_number = avoided_number
    
    def __repr__(self):
        return "AG{}".format(str(self.formula1))
        
    def evaluate(self, variables):
        result = min(self.accumulated_result, self.formula1.evaluate(variables)[0] * eta(self.avoided_number))
        return (
            result,
            [
                AlmostAlways(self.formula1, result, self.avoided_number),
                AlmostAlways(self.formula1, self.accumulated_result, self.avoided_number + 1)
            ]
        )

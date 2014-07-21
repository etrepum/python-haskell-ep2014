class AST(object):
    def eval(self):
        raise NotImplementedError

class Constant(AST):
    def __init__(self, value):
        self.value = value

    def eval(self):
        return self.value

class Minus(AST):
    def __init__(self, node):
        self.node = node

    def eval(self):
        return self.node.eval()

class Add(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() + self.right.eval()

class Multiply(AST):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def eval(self):
        return self.left.eval() * self.right.eval()

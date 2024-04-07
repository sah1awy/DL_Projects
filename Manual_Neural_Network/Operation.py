import numpy as np


class Operation():
    def __init__(self, input_nodes=[]):
        self.input_nodes = input_nodes  # The list of input nodes
        self.output_nodes = []  # List of nodes consuming this node's output

        # For every node in the input, we append this operation (self) to the list of
        # the consumers of the input nodes
        for node in input_nodes:
            node.output_nodes.append(self)

        # There will be a global default graph
        # We will then append this particular operation
        # Append this operation to the list of operations in the currently active default graph
        _default_graph.operations.append(self)

    def compute(self):

        pass


class add(Operation):

    def __init__(self, x, y):
        super().__init__([x, y])

    def compute(self, x_var, y_var):
        self.inputs = [x_var, y_var]
        return x_var + y_var

class multiply(Operation):

    def __init__(self, a, b):
        super().__init__([a, b])

    def compute(self, a_var, b_var):
        self.inputs = [a_var, b_var]
        return a_var * b_var


class matmul(Operation):

    def __init__(self, a, b):
        super().__init__([a, b])

    def compute(self, a_mat, b_mat):
        self.inputs = [a_mat, b_mat]
        return a_mat.dot(b_mat)


class Placeholder():


    def __init__(self):
        self.output_nodes = []

        _default_graph.placeholders.append(self)


class Variable():
    """
    This variable is a changeable parameter of the Graph.
    """

    def __init__(self, initial_value=None):
        self.value = initial_value
        self.output_nodes = []

        _default_graph.variables.append(self)


class Graph():

    def __init__(self):
        self.operations = []
        self.placeholders = []
        self.variables = []

    def set_as_default(self):
        global _default_graph
        _default_graph = self


def traverse_postorder(operation):

    nodes_postorder = []

    def recurse(node):
        if isinstance(node, Operation):
            for input_node in node.input_nodes:
                recurse(input_node)
        nodes_postorder.append(node)

    recurse(operation)
    return nodes_postorder


class Session:

    def run(self, operation, feed_dict={}):

        # Puts nodes in correct order
        nodes_postorder = traverse_postorder(operation)

        for node in nodes_postorder:

            if type(node) == Placeholder:

                node.output = feed_dict[node]

            elif type(node) == Variable:

                node.output = node.value

            else:  # Operation

                node.inputs = [input_node.output for input_node in node.input_nodes]

                node.output = node.compute(*node.inputs)

            # Convert lists to numpy arrays
            if type(node.output) == list:
                node.output = np.array(node.output)

        # Return the requested node value
        return operation.output


class Sigmoid(Operation):

    def __init__(self, z):
        # a is the input node
        super().__init__([z])

    def compute(self, z_val):
        return 1 / (1 + np.exp(-z_val))
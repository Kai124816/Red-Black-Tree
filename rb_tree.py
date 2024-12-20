
class Node(object):
    """
    A node on a red black tree

    ...

    Attributes
    ----------
    data: int
        Value the node holds
    self.left: Node
        The node's left child
    self.right: Node
        The node's right child
    self.parent: Node
        The node's parent
    self.color: str
        The node's color
    """
    def __init__(self, data, left=None, right=None, parent=None, color='red'):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.color = color


class rb_tree(object):
    """
    A red black tree.

    ...

    Attributes
    ----------
    Preorder: int
        For traversing tree in preorder
    Inorder: int
        For traversing tree in inorder
    Postorder: int
        For traversing tree in postorder
    self.root: Node
        Root of the tree
    self.sentinel: Null node

    Methods
    -------
    print_tree():
        Print the data of all nodes in order
    __print_tree(arg1=curr_node):
        Helper function for print_tree
    print_with_colors():
        Prints the data and colors of all nodes in order 
    __print_with_colors(arg1=curr_node):
        Helper function for print_with_colors
    __iter__():
        iterates through tree
    inorder():
        A inorder traversal of the tree
    preorder():
        A preorder traversal of the tree
    postorder():
        A postorder traversal of the tree
    __traverse(arg1 = curr_node, arg2 = traversal type):
        Helper function for tree traversals
    find_min():
        Finds node with minimum value in tree
    find_node(arg1 = data):
        Finds node with value specified by data
    __get(arg1=data, arg2=current_node):
        Helper function for find_node
    find_successor(arg1=data):
        Finds the successor of the node with the given data
    insert(arg1=data):
        Insert a node that contains the given data into the tree
    bst_insert(arg1=data):
        Inserts a node as you would in a binary search tree
    __put(arg1=data, arg2=current_node):
        Helper function for insert that finds appropriate place to put a node in the tree
    left_rotate(arg1 = x):
        Rotates node to the left
    right_rotate(arg1 = x):
        Rotates node to the right
    __rb_insert_fixup(arg1 = z):
        Fixes tree to after a node is inserted
    replace(arg1 = original,arg2 = replacer):
        Replaces one node(original) with another(replacer)
    delete(arg1 = data):
        Deletes node with given data as would in a binary search tree
    __rb_delete_fixup(arg1 = x):
        Fixes tree after node is deleted   
    """

    PREORDER = 1
    INORDER = 2
    POSTORDER = 3

    # Initialize root and size
    def __init__(self):
        self.root = None
        self.sentinel = Node(None, color='black')
        self.sentinel.parent = self.sentinel
        self.sentinel.left = self.sentinel
        self.sentinel.right = self.sentinel

    def print_tree(self):
        # Print the data of all nodes in order
        self.__print_tree(self.root)
        print()

    def __print_tree(self, curr_node):
        # Recursively print a subtree (in order), rooted at curr_node
        # Printed in preorder
        if curr_node is not self.sentinel:
            print(str(curr_node.data), end=' ')  # save space
            self.__print_tree(curr_node.left)
            self.__print_tree(curr_node.right)

    def __print_with_colors(self, curr_node):
        # Recursively print a subtree (in order), rooted at curr_node
        # Printed in PREORDER
        # Extracts the color of the node and print it in the format -dataC-
        # where C is B for black and R for red
        if curr_node is not self.sentinel:
            node_color = "R" if curr_node.color == "red" else "B"
            print(str(curr_node.data) + node_color, end=' ')  # save space
            self.__print_with_colors(curr_node.left)
            self.__print_with_colors(curr_node.right)

    def print_with_colors(self):
        # Also prints the data of all node but with color indicators
        self.__print_with_colors(self.root)

    def __iter__(self):
        return self.inorder()

    def inorder(self):
        return self.__traverse(self.root, rb_tree.INORDER)

    def preorder(self):
        return self.__traverse(self.root, rb_tree.PREORDER)

    def postorder(self):
        return self.__traverse(self.root, rb_tree.POSTORDER)

    def __traverse(self, curr_node, traversal_type):
        if curr_node is not self.sentinel:
            if traversal_type == self.PREORDER:
                yield curr_node
            yield from self.__traverse(curr_node.left, traversal_type)
            if traversal_type == self.INORDER:
                yield curr_node
            yield from self.__traverse(curr_node.right, traversal_type)
            if traversal_type == self.POSTORDER:
                yield curr_node

    # find_min travels across the leftChild of every node,
    # and returns the node who has no leftChild. This is the min value of a subtree
    def find_min(self):
        current_node = self.root
        while current_node.left is not self.sentinel:
            current_node = current_node.left
        return current_node

    # find_node expects a data and returns the Node object for the given data
    def find_node(self, data):
        if self.root:
            res = self.__get(data, self.root)
            if res:
                return res
            else:
                raise KeyError('Error, data not found')
        else:
            raise KeyError('Error, tree has no root')

    # Helper function __get receives a data and a node. Returns the node with the given data
    def __get(self, data, current_node):
        if current_node is self.sentinel:  # if current_node does not exist return None
            print("couldn't find data: {}".format(data))
            return None
        elif current_node.data == data:
            return current_node
        elif data < current_node.data:
            # Recursively call __get with data and current_node's left
            return self.__get(data, current_node.left)
        else:  # data is greater than current_node.data
            # Recursively call __get with data and current_node's right
            return self.__get(data, current_node.right)

    def find_successor(self, data):
        # Private Method, can only be used inside of BST.
        current_node = self.find_node(data)
        if current_node is self.sentinel:
            raise KeyError
        # Travel left down the rightmost subtree
        if current_node.right:
            current_node = current_node.right
            while current_node.left is not self.sentinel:
                current_node = current_node.left
            successor = current_node
        # Travel up until the node is a left child
        else:
            parent = current_node.parent
            while parent is not self.sentinel and current_node is not parent.left:
                current_node = parent
                parent = parent.parent
            successor = parent
        if successor:
            return successor
        else:
            return None

    # put adds a node to the tree
    def insert(self, data):
        # if the tree has a root
        if self.root and self.root != self.sentinel:
            # use helper method __put to add the new node to the tree
            new_node = self.__put(data, self.root)
            self.__rb_insert_fixup(new_node)
        else:  # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent=self.sentinel, left=self.sentinel, right=self.sentinel)
            new_node = self.root
            self.__rb_insert_fixup(new_node)

    # Insertion for Binary Search Tree
    def bst_insert(self, data):
        # if the tree has a root
        if self.root and self.root != self.sentinel:
            # use helper method __put to add the new node to the tree
            self.__put(data, self.root)
        else:  # there is no root
            # make root a Node with values passed to put
            self.root = Node(data, parent=self.sentinel, left=self.sentinel, right=self.sentinel)

    # Helper function __put finds the appropriate place to add a node in the tree
    def __put(self, data, current_node):
        if data < current_node.data:
            if current_node.left != self.sentinel:
                new_node = self.__put(data, current_node.left)
            else:  # current_node has no child
                new_node = Node(data, parent=current_node, left=self.sentinel, right=self.sentinel)
                current_node.left = new_node
        else:  # data is greater than or equal to current_node's data
            if current_node.right != self.sentinel:
                new_node = self.__put(data, current_node.right)
            else:  # current_node has no right child
                new_node = Node(data, parent=current_node, left=self.sentinel, right=self.sentinel)
                current_node.right = new_node
        return new_node
        
    def left_rotate(self,x:Node):
        """
        Rotates the node x to the left and modifies other nodes based on this rotation

        Parameters
        ----------
        x : Node
            Node that is being rotated

        Raises
        ------
        Keyerror
            If x's right child is null node because left rotation is impossible
            if the node's right child is null
        """
        if x.right == self.sentinel:
            raise KeyError
        y = x.right
        x.right = y.left
        if y.left != self.sentinel:
            y.left.parent = x
        y.parent = x.parent
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.left = x
        x.parent = y

    def right_rotate(self,x:Node):
        """
        Rotates the node x to the right and modifies other nodes based on this rotation

        Parameters
        ----------
        x : Node
            Node that is being rotated

        Raises
        ------
        Keyerror
            If x's left child is null node because right rotation is impossible
            if the node's left child is null
        """
        if x.left == self.sentinel:
            raise KeyError
        y = x.left
        x.left = y.right
        if y.right != self.sentinel:
            y.right.parent = x
        y.parent = x.parent
        if x.parent == self.sentinel:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
        y.right = x
        x.parent = y

    def __rb_insert_fixup(self, z:Node):
        """
        Makes sure the tree is a legal red black tree after a 
        new node is inserted, using rotations and recoloring.

        Parameters
        ----------
        Z : Node
            Node that was just inserted and needs to be adjusted
            to maintain rb tree properties
        """
        # Maintains balancing and coloring property after BST insertion
        while z.parent.color == 'red':
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else: 
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                if y.color == 'red':
                    z.parent.color = 'black'
                    y.color = 'black'
                    z.parent.parent.color = 'red'
                    z = z.parent.parent
                else: 
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = 'black'
                    z.parent.parent.color = 'red'
                    self.left_rotate(z.parent.parent)
        self.root.color = 'black'

    def replace(self,original:Node,replacer:Node):
        """
        Replaces Node 'originial' in the tree with Node 'replacer

        Parameters
        ----------
        original : Node
            Node that is being replaced
        replacer : Node
            Node that is replacing original
        """
        if original.parent == self.sentinel:
            self.root = replacer
            replacer.parent = self.sentinel
        else:
            if original == original.parent.left:
                original.parent.left = replacer
            else:
                original.parent.right = replacer
            replacer.parent = original.parent

    def delete(self, data):
        """
        Deletes node with given data as you would delete a node in a binary search tree

        Parameters
        ----------
        data : int, optional
            The value we are deleting from the tree

        Raises
        ------
        KeyError
            If tree is empty
        KeyError
            If node with given data does not exist in the tree
        """
        # Same as binary tree delete, except we call rb_delete fixup at the end.
        if not self.root:
            raise KeyError
        node = self.find_node(data)
        
        original_color = node.color
        if node.left == self.sentinel:
            x = node.right
            self.replace(node,node.right)
        elif node.right == self.sentinel:
            x = node.left
            self.replace(node,node.left)
        else:
            successor = self.find_successor(node.data)
            original_color = successor.color
            x = successor.right
            if successor.parent == node:
                x.parent = successor
            else:
                self.replace(successor,successor.right)
                successor.right = node.right
                successor.right.parent = successor
            self.replace(node,successor)
            successor.left = node.left
            successor.left.parent = successor
            successor.color = node.color
        if original_color == 'black':
            self.__rb_delete_fixup(x)

    def __rb_delete_fixup(self, x:Node):
        # Maintains balancing and coloring property after BST deletion
        """
        Makes sure the tree is a legal red black tree after a
        node is deleted, using rotations and recoloring.

        Parameters
        ----------
        X : Node
            Node that needs to be adjusted in order to maintain
            rb tree properties.
        """
        while x != self.root and x.color == 'black':
            if x == x.parent.left:
                w = x.parent.right
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.left_rotate(x.parent)
                    w = x.parent.right
                if w.left.color == 'black' and w.right.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.right.color == 'black':
                        w.left.color = 'black'
                        w.color = 'red'
                        self.right_rotate(w)
                        w = x.parent.right
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.right.color = 'black'
                    self.left_rotate(x.parent)
                    x = self.root
            else:
                w = x.parent.left
                if w.color == 'red':
                    w.color = 'black'
                    x.parent.color = 'red'
                    self.right_rotate(x.parent)
                    w = x.parent.left
                if w.right.color == 'black' and w.left.color == 'black':
                    w.color = 'red'
                    x = x.parent
                else:
                    if w.left.color == 'black':
                        w.right.color = 'black'
                        w.color = 'red'
                        self.left_rotate(w)
                        w = x.parent.left
                    w.color = x.parent.color
                    x.parent.color = 'black'
                    w.left.color = 'black'
                    self.right_rotate(x.parent)
                    x = self.root
        x.color = 'black'



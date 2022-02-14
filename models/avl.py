from models.node import Node
from models.bst import BST
# from models.hotel import Hotel


class AVL(BST):

    @staticmethod
    def max(x_height, y_height):
        return x_height if x_height > y_height else y_height

    @staticmethod
    def get_height(point: Node):
        if point is None:
            return -1
        return point.height

    @staticmethod
    def update_height(point: Node):
        point.height = 1 + max(
            AVL.get_height(point.left), AVL.get_height(point.right)
        )

    @staticmethod
    def get_balance(point: Node):
        left_h = AVL.get_height(point.left)
        right_h = AVL.get_height(point.right)

        b_fact = left_h - right_h

        return b_fact

    @staticmethod
    def get_min(point: Node):
        temp = point
        while temp.left is not None:
            temp = temp.left
        return temp

    def right_rotate(self, point: Node):
        par: Node = point.parent
        g_par: Node = par.parent
        if g_par is not None:
            if g_par.left is par:
                g_par.left = point
            else:
                g_par.right = point
        elif self.root is par:
            self.root = point

        point.parent = g_par
        par.left = point.right
        point.right = par
        par.height = 1 + self.max(
            self.get_height(par.left), self.get_height(par.right)
        )
        point.height = 1 + self.max(
            self.get_height(point.left), self.get_height(point.right)
        )

    def left_rotate(self, point: Node):
        par: Node = point.parent
        g_par: Node = par.parent
        if g_par is not None:
            if g_par.left is par:
                g_par.left = point
            else:
                g_par.right = point
        elif self.root is par:
            self.root = point

        point.parent = g_par
        par.right = point.left
        point.left = par
        par.height = 1 + self.max(
            self.get_height(par.left), self.get_height(par.right)
        )
        point.height = 1 + self.max(
            self.get_height(point.left), self.get_height(point.right)
        )

    def balance_add(self, point: Node, key_l):
        self.update_height(point)
        p_left_l = None
        if point.left is not None:
            p_left_l = point.left.data.word.lower()
        p_right_l = None
        if point.right is not None:
            p_right_l = point.right.data.word.lower()

        b_fact = self.get_balance(point)
        if b_fact > 1 and key_l < p_left_l:
            self.right_rotate(point.left)
        elif b_fact < -1 and key_l > p_right_l:
            self.left_rotate(point.right)
        elif b_fact > 1 and key_l > p_left_l:
            self.left_rotate(point.left.right)
            self.right_rotate(point.left)
        elif b_fact < -1 and key_l < p_right_l:
            self.right_rotate(point.right.left)
            self.left_rotate(point.right)

    def balance_del(self, point: Node):
        self.update_height(point)
        b_fact = self.get_balance(point)

        axel = None
        if b_fact > 1 and self.get_balance(point.left) >= 0:
            axel = point.left
            self.right_rotate(axel)
        elif b_fact < -1 and self.get_balance(point.right) <= 0:
            axel = point.right
            self.left_rotate(axel)
        elif b_fact > 1 and self.get_balance(point.left) < 0:
            axel = point.left.right
            self.left_rotate(axel)
            self.right_rotate(point.left)
        elif b_fact < -1 and self.get_balance(point.right) > 0:
            axel = point.right.left
            self.right_rotate(axel)
            self.left_rotate(point.right)
        return axel

    def push(self, obj, key, point: Node):

        new_node: Node = Node(obj)

        if point is None:
            self.root = new_node
            return

        key_l = key.lower()
        point_l = point.data.word.lower()

        if key_l < point_l:
            if point.left is None:
                new_node.parent = point
                point.left = new_node
            else:
                self.push(obj, key, point.left)
        elif key_l > point_l:
            if point.right is None:
                point.right = new_node
            else:
                self.push(obj, key, point.right)
        # Update
        else:
            point.data = new_node.data

        self.balance_add(point, key_l)

    def avl_insert(self, obj, key) -> bool:
        if self.search_node(key) is not None:
            print('Word already exists')
            return False

        self.push(obj, key, self.root)
        return True

    def avl_update(self, obj, key) -> bool:
        if self.search_node(key) is None:
            print('Word does not exists')
            return False

        self.push(obj, key, self.root)
        return True

    def del_from_point(self, point: Node, key_l) -> Node:
        if not point:
            return point

        point_l = point.data.word.lower()

        if key_l < point_l:
            point.left = self.del_from_point(point.left, key_l)
        elif key_l > point_l:
            point.right = self.del_from_point(point.right, key_l)

        else:
            if point.left is None:
                temp = point.right
                point = None
                return temp
            elif point.right is None:
                temp = point.left
                point = None
                return temp
            else:
                io_suc: Node = self.get_min(point.right)
                point.data = io_suc.data
                point.right = self.del_from_point(
                    point.right, io_suc.data.word.lower()
                )

        if point is None:
            return point

        rotor = self.balance_del(point)

        return point if rotor is None else rotor

    def avl_delete(self, key: str) -> bool:
        to_del = self.search_node(key)

        if to_del is None:
            return False

        self.root = self.del_from_point(self.root, key.lower())

        return True

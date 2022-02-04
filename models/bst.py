from models.node import Node
from models.vucab import Vucab


class BST:
    def __init__(self):
        self.__root = None

    def _get_root(self) -> Node:
        return self.__root

    def _set_root(self, node) -> None:
        self.__root = node

    @staticmethod
    def _search_leaf_with_parent(node: Node, parent: Node):

        leaf_parent = parent
        leaf = node
        is_left = False

        if leaf is not None:

            reached_leaf = False

            while not reached_leaf:
                if leaf.left is None and leaf.right is None:
                    reached_leaf = True
                elif leaf.left is not None:
                    leaf_parent = leaf
                    leaf = leaf.left
                    is_left = True
                elif leaf.right is None:
                    leaf_parent = leaf
                    leaf = leaf.right
                    is_left = False

        return [leaf, leaf_parent, is_left]

    def _search_node_with_parent(self, word: str):
        parent = None
        node = self.root
        is_left = None

        word_l = word.lower()

        while node is not None:
            node_word_l = node.data.word.lower()

            if word_l == node_word_l:
                break

            parent = node
            if word_l < node_word_l:
                is_left = True
                node = node.left
            elif word_l > node_word_l:
                is_left = False
                node = node.right

        return [node, parent, is_left]

    def search_node(self, word: str) -> Node:
        node = self.root
        result = None
        word_l = word.lower()

        while node is not None:
            node_word_l = node.data.word.lower()

            if word_l == node_word_l:
                result = node
                break

            if word_l < node_word_l:
                node = node.left
            elif word_l > node_word_l:
                node = node.right

        return result

    def insert_from_point(self, val: Vucab, point: Node) -> None:
        if self.search_node(val.word) is None:

            new_node: Node = Node(val)

            if point is None:
                self.root = new_node
                return

            vucab_word_l = val.word.lower()
            point_word_l = point.data.word.lower()

            if vucab_word_l < point_word_l:
                if point.left is None:
                    point.left = new_node
                else:
                    self.insert_from_point(val, point.left)
            elif vucab_word_l > point_word_l:
                if point.right is None:
                    point.right = new_node
                else:
                    self.insert_from_point(val, point.right)
        else:
            print('Word already exists')

    def insert(self, val):
        self.insert_from_point(val, self.root)

    def delete_node(self, word) -> bool:
        [to_del, parent, to_del_is_left] = self._search_node_with_parent(word)

        if to_del is None:
            return False

        if to_del.left is None or to_del.right is None:
            if parent is not None:
                if to_del.left is None:
                    if to_del_is_left:
                        parent.left = to_del.right
                    else:
                        parent.right = to_del.right
                else:
                    if to_del_is_left:
                        parent.left = to_del.left
                    else:
                        parent.right = to_del.left
            else:
                if to_del.left is None:
                    self.root = to_del.right
                else:
                    self.root = to_del.left

        elif to_del.left.right is None:
            to_del.left.right = to_del.right
            to_del.right = None
            if parent is not None:
                if to_del_is_left:
                    parent.left = to_del.left
                else:
                    parent.right = to_del.left
            else:
                self.root = to_del.left
        elif to_del.right.left is None:
            to_del.right.left = to_del.left
            to_del.left = None
            if parent is not None:
                if to_del_is_left:
                    parent.left = to_del.right
                else:
                    parent.right = to_del.right
            else:
                self.root = to_del.right
        else:
            [predecessor, pre_parent, is_left] = self._search_leaf_with_parent(
                to_del.left.right, to_del.left
            )
            to_del.data = predecessor.data

            if is_left:
                pre_parent.left = None
            else:
                pre_parent.right = None

        return True

    def display(self):
        self.display_in_order(self.root)

    def display_in_order(self, point: Node) -> None:
        if point is not None:
            self.display_in_order(point.left)
            point.display()
            print()
            self.display_in_order(point.right)

    root = property(_get_root, _set_root)

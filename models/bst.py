from models.node import Node


class BST:
    def __init__(self):
        self._root = None

    def _get_root(self) -> Node:
        return self._root

    def _set_root(self, node) -> None:
        self._root = node

    @staticmethod
    def _search_leaf_with_parent(node: Node):

        leaf = node

        if leaf is not None:

            reached_leaf = False

            while not reached_leaf:
                if leaf.left is None and leaf.right is None:
                    reached_leaf = True
                elif leaf.left is not None:
                    leaf = leaf.left
                elif leaf.right is None:
                    leaf = leaf.right

        is_left = True if leaf.parent.left is leaf else False
        return [leaf, leaf.parent, is_left]

    def search_node(self, key: str) -> Node:
        node = self.root
        result = None
        key_l = key.lower()

        while node is not None:
            node_l = node.data.word.lower()

            if key_l == node_l:
                result = node
                break

            if key_l < node_l:
                node = node.left
            elif key_l > node_l:
                node = node.right

        return result

    def insert_from_point(self, obj, key, point: Node, is_first=True) -> None:
        if is_first:
            if self.search_node(key) is not None:
                print('Word already exists')
                return

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
                self.insert_from_point(obj, key, point.left, False)
        elif key_l > point_l:
            if point.right is None:
                new_node.parent = point
                point.right = new_node
            else:
                self.insert_from_point(obj, key, point.right, False)

    def insert(self, obj, key) -> None:
        self.insert_from_point(obj, key, self.root)

    def delete_node(self, key) -> bool:
        to_del = self.search_node(key)
        parent = to_del.parent
        to_del_is_left = True if parent.left is to_del else False

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
                to_del.left.right
            )
            to_del.data = predecessor.data

            if is_left:
                pre_parent.left = None
            else:
                pre_parent.right = None

        return True

    def display_in_order(self, point: Node) -> None:
        if point is not None:
            self.display_in_order(point.left)
            point.display()
            print()
            self.display_in_order(point.right)

    root = property(_get_root, _set_root)

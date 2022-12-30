"Implements a doubly linked list as a series of nodes. Optionally can be circular."

from typing import Any
from lib.shared import sgn

class Node:
    def __init__(self, val, circular_list=False):#, head=None, tail= None):
        self.value = val
        if circular_list:
            pointer = self
        else:
            pointer = None
        self.next: Node = pointer
        self.prev: Node = pointer
        # if head is None:
        #     self.head: Node = pointer
        # if tail is None:
        #     self.tail: Node = pointer
    def insert_after(self, val) -> 'Node':
        b = self.__class__(val)
        c = self.next
        if c is not None:
            c.prev = b        
        b.prev = self
        b.next = c
        self.next = b
        return b
    def insert_before(self, val) -> 'Node':
        b = self.__class__(val)
        a = self.prev
        if a is not None:
            a.next = b        
        b.prev = a
        b.next = self
        self.prev = b
        return b
    def delete(self) -> Any:
        a, c = self.prev, self.next
        if a is not None:
            a.next = c
        if c is not None:
            c.prev = a
        return self.value
    def move(self, offset) -> 'Node':
        if offset == 0:
            return self
        if offset < 0:
            c = self.get_offset_loop(offset)
            if c is None:
                return
            a = None if c is None else c.prev
        if offset > 0:
            a = self.get_offset_loop(offset)
            if a is None:
                return
            c = None if a is None else a.next
        self.delete()
        if c:
            c.prev = self
        self.next = c
        if a:            
            a.next = self
        self.prev = a
        return self
                       
    def get_offset(self, offset) -> 'Node':
        if offset == 0:
            return self
        elif offset > 0:
            if self.next is not None:
                return self.next.get_offset(offset-1)
        elif offset < 0:
            if self.prev is not None:
                return self.prev.get_offset(offset+1)
                
    def get_offset_loop(self, offset) -> 'Node':
        if offset == 0:
            return self
        pointer = self
        if offset > 0:
            for i in range(0,offset):
                pointer = pointer.next
                if pointer is None:
                    return pointer
            return pointer
        if offset < 0:
            for i in range(0, offset, -1):
                pointer = pointer.prev
                if pointer is None:
                    return pointer
            return pointer
    def __iter__(self):
        start = self
        yield self
        node = start.next
        while node != start:
            yield node
            if node.next is not None:
                node = node.next
            else:
                break
    def __repr__(self):
        return f'Node({self.value})'
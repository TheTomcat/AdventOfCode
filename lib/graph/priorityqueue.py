from typing import TypeVar, List, Tuple, Generic
import heapq as hq
from collections import deque

T = TypeVar('T')

# Adapted largely from https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Amit Patel, Red Blob Games

class PriorityQueue(Generic[T]):
    """A priority queue.
    """
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.elements: List[Tuple[float, T]] = elements
    def is_empty(self) -> bool:
        return not self.elements
    def put(self, item: T, priority: float):
        hq.heappush(self.elements, (priority, item))
    def get(self) -> T:
        return hq.heappop(self.elements)[1]
    def get_with_priority(self) -> Tuple[float, T]:
        return hq.heappop(self.elements)
    def __len__(self):
        return len(self.elements)

class Queue(Generic[T]):
    def __init__(self):
        self.elements = deque()
    def is_empty(self) -> bool:
        return not self.elements
    def put(self, x: T):
        self.elements.append(x)
    def putleft(self, x: T):
        self.elements.appendleft(x)
    def get(self) -> T:
        return self.elements.popleft()
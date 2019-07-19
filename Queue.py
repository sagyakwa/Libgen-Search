from collections import deque


class Queue:
    '''
    Thread-safe, memory-efficient, maximally-sized queue supporting queueing and
    dequeueing in worst-case O(1) time.
    '''

    def __init__(self, max_size=100):  # Initialize this queue to the empty queue.
        self._queue = deque(maxlen=max_size)

    def enqueue(self, item):  # Queues the passed item
        self._queue.append(item)

    def dequeue(self):  # Dequeues (i.e., removes) the item at the head of this queue *and* returns this item.
        return self._queue.pop()
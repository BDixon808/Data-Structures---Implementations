
from include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0


    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Puts item into hashmap
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        tl = self.table_load()
        if self._size > 0:
            l = self._buckets[index].length()
            if l > 0:
                for num in range(self._buckets[index].length()):
                    if self._buckets[index].contains(key) is not None:
                        k = self._buckets[index].contains(key).key
                        if k == key:
                            self._buckets[index].contains(key).value = value

                    else:
                        self._buckets[index].insert(key, value)
                        self._size += 1
            else:
                self._buckets[index].insert(key, value)
                self._size += 1
        else:
            self._buckets[index].insert(key, value)
            self._size += 1
        if tl >= 1.00:
            self.resize_table(self._capacity * 2)

    def empty_buckets(self) -> int:
        """
        Returns the empty buckets
        """
        buckets = 0
        for num in range(self._capacity):
            if self._buckets[num].length() == 0:
                buckets += 1
        return buckets

    def table_load(self) -> float:
        """
        Returns the current table load
        """
        return self._size / self._capacity

    def clear(self) -> None:
        """
        Clears the hashmap
        """
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(self._capacity):
            self._buckets.append(LinkedList())

    def valid_table(self):
        """
        Checks if table is valid if not resizes
        """
        tl = self.table_load()
        if tl > 1.00:
            self.resize_table(self._capacity * 2)

    def resize_table(self, new_capacity: int) -> None:
        """
        Resizes the hashmap
        """
        if new_capacity < 1:
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        old_capacity = self._capacity
        if self._is_prime(new_capacity):
            self._capacity = new_capacity
        else:
            new_capacity = self._next_prime(new_capacity)
            self._capacity = new_capacity
        old_buckets = self._buckets
        new_buckets = DynamicArray()
        self._buckets = new_buckets
        for num in range(self._capacity):
            self._buckets.append(LinkedList())
        # need to rehash
        for num in range(old_buckets.length()):
            if old_buckets[num].length() > 0:
                for node in old_buckets[num]:
                    hash = self._hash_function(node.key)
                    index = hash % self._capacity
                    self._buckets[index].insert(node.key, node.value)
        self.valid_table()

    def get(self, key: str):
        """
        gets item in the hashmap
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index].length == 0:
            return None
        node = self._buckets[index].contains(key)
        if node is not None:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Check is item is in hashmap
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index].length == 0:
            return False
        else:
            if self._buckets[index].contains(key) is not None:
                return True
            else:
                return False

    def remove(self, key: str) -> None:
        """
        Removes item from the hashmap
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        ll = self._buckets[index]
        t = ll.remove(key)
        if t is True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns all key value pairs in hashmap
        """
        arr = DynamicArray()
        for num in range(self._capacity):
            bucket = self._buckets[num]
            for node in bucket:
                arr.append((node.key, node.value))
        return arr


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Finds mode in hashmap
    """
    # if you'd like to use a hash map,
    # use this instance of your Separate Chaining HashMap
    arr = DynamicArray()
    map = HashMap()
    freq = 0
    for num in range(da.length()):
        map.put(str(da[num]), 0)
    for num in range(da.length()):
        if map.contains_key(da[num]):
            frequency = map.get(da[num])
            frequency += 1
            map.put(da[num], frequency)
    comp = 0
    for num in range(da.length()):
        item = da[num]
        check = map.get(str(item))
        if check > comp:
            comp = check

    for num in range(da.length()):
        item = da[num]
        check = map.get(str(item))
        if check == comp:
            arr.append(item)
            map.remove(item)

    for num in range(arr.length() - 1):
        if arr[num] > arr[num + 1]:
            arr.swap(num, num + 1)

    return arr, comp

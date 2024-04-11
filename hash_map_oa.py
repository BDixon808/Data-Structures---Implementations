# Name: Brett Dixon
# OSU Email: dixonbre@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 8/15/2023
# Description: Hashmap

from include import (DynamicArray, DynamicArrayException, HashEntry,
                        hash_function_1, hash_function_2)


class HashMapException(Exception):
    """exception for iteration"""
    pass


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

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
        Increment from given number to find the closest prime number
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
        Add item to map
        """
        tl = self.table_load()
        if tl >= 0.5:
            self.resize_table(self._capacity * 2)
        hash = self._hash_function(key)
        index = hash % self._capacity
        entry = HashEntry(key, value)
        if self._buckets[index] is None:
            self._buckets[index] = entry
            self._size += 1
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].value = value
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is True:
            self._buckets[index].value = value
            self._buckets[index].is_tombstone = False
            self._size += 1
        else:
            j = 1
            qp = (index + j ** 2) % self._capacity
            # need to handle update value if key already in map while QP
            while self._buckets[qp] is not None:
                if self._buckets[qp].key == key and self._buckets[qp].is_tombstone is False:
                    self._buckets[qp].value = value
                    break
                elif self._buckets[qp].key == key and self._buckets[qp].is_tombstone is True:
                    self._buckets[qp].value = value
                    self._buckets[qp].is_tombstone = False
                    self._size += 1
                    break
                elif self._buckets[qp] is None:
                    self._buckets[qp] = entry
                    self._size += 1
                j += 1
                qp = (index + j ** 2) % self._capacity
            if self._buckets[qp] is None:
                self._buckets[qp] = entry
                self._size += 1

    def table_load(self) -> float:
        """
        returns table load
        """
        return self._size / self._capacity

    def empty_buckets(self) -> int:
        """
        return number of empty buckets
        """
        empty_buckets = self._capacity - self._size
        return empty_buckets

    def valid_table(self):
        """
        Checks if table is valid if not resizes
        """
        tl = self.table_load()
        if tl > 0.5:
            self.resize_table(self._capacity * 2)

    def resize_table(self, new_capacity: int) -> None:
        """
        resizes the hashmap
        """
        if new_capacity < self._size:
            return
        old_buckets = self._buckets
        old_cap = self._capacity
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        self._capacity = new_capacity
        new_buckets = DynamicArray()
        for num in range(self._capacity):
            new_buckets.append(None)
        self._buckets = new_buckets
        b = old_buckets.length()
        # maybe use while loop with QP to traverse
        for num in range(old_cap):
            if old_buckets[num] is not None and old_buckets[num].is_tombstone is False:
                hash = self._hash_function(old_buckets[num].key)
                index = hash % self._capacity
                # handle collisions
                if self._buckets[index] is None:
                    self._buckets[index] = old_buckets[num]
                else:
                    j = 1
                    qp = (index + j ** 2) % self._capacity
                    while self._buckets[qp] is not None:
                        j += 1
                        qp = (index + j ** 2) % self._capacity
                    self._buckets[qp] = old_buckets[num]
        self.valid_table()

    def get(self, key: str) -> object:
        """
        returns value at specified key
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key:
            if not self._buckets[index].is_tombstone:
                return self._buckets[index].value
            else:
                return
        else:
            j = 1
            qp = (index + j ** 2) % self._capacity
            while self._buckets[qp] is not None and qp < self._buckets.length():
                if self._buckets[qp].key == key:
                    return self._buckets[qp].value
                j += 1
                qp = (index + j ** 2) % self._capacity
            return

    def contains_key(self, key: str) -> bool:
        """
        Retuens true if the map contains the key
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return False
        elif self._buckets[index].key == key:
            if not self._buckets[index].is_tombstone:
                return True
            else:
                return False
        else:
            j = 1
            qp = (index + j ** 2) % self._capacity
            while self._buckets[qp] is not None:
                if self._buckets[qp].key == key and self._buckets[qp].is_tombstone is False:
                    return True
                j += 1
                qp = (index + j ** 2) % self._capacity
            return False

    def remove(self, key: str) -> None:
        """
        removes the item from the map
        """
        hash = self._hash_function(key)
        index = hash % self._capacity
        if self._buckets[index] is None:
            return
        elif self._buckets[index].key == key and self._buckets[index].is_tombstone is False:
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return
        else:
            j = 1
            qp = (index + j ** 2) % self._capacity
            while self._buckets[qp] is not None:
                if self._buckets[qp].key == key and self._buckets[index].is_tombstone is False:
                    self._buckets[qp].is_tombstone = True
                    self._size -= 1
                j += 1
                qp = (index + j ** 2) % self._capacity
            return

    def clear(self) -> None:
        """
        Clear the map
        """
        new_buckets = DynamicArray()
        for num in range(self._capacity):
            new_buckets.append(None)
        self._buckets = new_buckets
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        Returns all key value pairs
        """
        arr = DynamicArray()
        for bucket in range(self._capacity):
            if self._buckets[bucket] is not None and self._buckets[bucket].is_tombstone is False:
                key = self._buckets[bucket].key
                value = self._buckets[bucket].value
                kvp = (key, value)
                arr.append(kvp)
        return arr

    def __iter__(self):
        """
        Start iteration
        """
        self._index = 0
        return self

    def __next__(self):
        """
        next iteration
        """
        try:
            item = self._buckets[self._index]
        except HashMapException:
            raise StopIteration
        while item is None and self._index < self._size:
            self._index = self._index + 1
            item = self._buckets[self._index]

        self._index = self._index + 1
        if item is None:
            raise StopIteration
        else:
            return item

# ------------------- BASIC TESTING ---------------------------------------- #

# if __name__ == "__main__":

# print("\nPDF - put example 1")
# print("-------------------")
# m = HashMap(53, hash_function_1)
# for i in range(150):
#     m.put('str' + str(i), i * 100)
#     if i % 25 == 24:
#         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
#
# print("\nPDF - put example 2")
# print("-------------------")
# m = HashMap(41, hash_function_2)
# for i in range(50):
#     m.put('str' + str(i // 3), i * 100)
#     if i % 10 == 9:
#         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
#
# print("\nPDF - table_load example 1")
# print("--------------------------")
# m = HashMap(101, hash_function_1)
# print(round(m.table_load(), 2))
# m.put('key1', 10)
# print(round(m.table_load(), 2))
# m.put('key2', 20)
# print(round(m.table_load(), 2))
# m.put('key1', 30)
# print(round(m.table_load(), 2))
#
# print("\nPDF - table_load example 2")
# print("--------------------------")
# m = HashMap(53, hash_function_1)
# for i in range(50):
#     m.put('key' + str(i), i * 100)
#     if i % 10 == 0:
#         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
#
# print("\nPDF - empty_buckets example 1")
# print("-----------------------------")
# m = HashMap(101, hash_function_1)
# print(m.empty_buckets(), m.get_size(), m.get_capacity())
# m.put('key1', 10)
# print(m.empty_buckets(), m.get_size(), m.get_capacity())
# m.put('key2', 20)
# print(m.empty_buckets(), m.get_size(), m.get_capacity())
# m.put('key1', 30)
# print(m.empty_buckets(), m.get_size(), m.get_capacity())
# m.put('key4', 40)
# print(m.empty_buckets(), m.get_size(), m.get_capacity())
#
# print("\nPDF - empty_buckets example 2")
# print("-----------------------------")
# m = HashMap(53, hash_function_1)
# for i in range(150):
#     m.put('key' + str(i), i * 100)
#     if i % 30 == 0:
#         print(m.empty_buckets(), m.get_size(), m.get_capacity())

# print("\nPDF - resize example 1")
# print("----------------------")
# m = HashMap(20, hash_function_1)
# m.put('key1', 10)
# print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
# m.resize_table(30)
# print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
#
# print("\nPDF - resize example 2")
# print("----------------------")
# m = HashMap(75, hash_function_2)
# keys = [i for i in range(25, 1000, 13)]
# for key in keys:
#     m.put(str(key), key * 42)
# print(m.get_size(), m.get_capacity())
#
# for capacity in range(111, 1000, 117):
#     m.resize_table(capacity)
#
#     if m.table_load() > 0.5:
#         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
#               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
#
#     m.put('some key', 'some value')
#     result = m.contains_key('some key')
#     m.remove('some key')
#
#     for key in keys:
#         # all inserted keys must be present
#         result &= m.contains_key(str(key))
#         # NOT inserted keys must be absent
#         result &= not m.contains_key(str(key + 1))
#     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

# print("\nPDF - get example 1")
# print("-------------------")
# m = HashMap(31, hash_function_1)
# print(m.get('key'))
# m.put('key1', 10)
# print(m.get('key1'))
#
# print("\nPDF - get example 2")
# print("-------------------")
# m = HashMap(151, hash_function_2)
# for i in range(200, 300, 7):
#     m.put(str(i), i * 10)
# print(m.get_size(), m.get_capacity())
# for i in range(200, 300, 21):
#     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
#     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
#
# print("\nPDF - contains_key example 1")
# print("----------------------------")
# m = HashMap(11, hash_function_1)
# print(m.contains_key('key1'))
# m.put('key1', 10)
# m.put('key2', 20)
# m.put('key3', 30)
# print(m.contains_key('key1'))
# print(m.contains_key('key4'))
# print(m.contains_key('key2'))
# print(m.contains_key('key3'))
# m.remove('key3')
# print(m.contains_key('key3'))
#
# print("\nPDF - contains_key example 2")
# print("----------------------------")
# m = HashMap(79, hash_function_2)
# keys = [i for i in range(1, 1000, 20)]
# for key in keys:
#     m.put(str(key), key * 42)
# print(m.get_size(), m.get_capacity())
# result = True
# for key in keys:
#     # all inserted keys must be present
#     result &= m.contains_key(str(key))
#     # NOT inserted keys must be absent
#     result &= not m.contains_key(str(key + 1))
# print(result)
#
# print("\nPDF - remove example 1")
# print("----------------------")
# m = HashMap(53, hash_function_1)
# print(m.get('key1'))
# m.put('key1', 10)
# print(m.get('key1'))
# m.remove('key1')
# print(m.get('key1'))
# m.remove('key4')
#
# print("\nPDF - clear example 1")
# print("---------------------")
# m = HashMap(101, hash_function_1)
# print(m.get_size(), m.get_capacity())
# m.put('key1', 10)
# m.put('key2', 20)
# m.put('key1', 30)
# print(m.get_size(), m.get_capacity())
# m.clear()
# print(m.get_size(), m.get_capacity())
#
# print("\nPDF - clear example 2")
# print("---------------------")
# m = HashMap(53, hash_function_1)
# print(m.get_size(), m.get_capacity())
# m.put('key1', 10)
# print(m.get_size(), m.get_capacity())
# m.put('key2', 20)
# print(m.get_size(), m.get_capacity())
# m.resize_table(100)
# print(m.get_size(), m.get_capacity())
# m.clear()
# print(m.get_size(), m.get_capacity())
#
# print("\nPDF - get_keys_and_values example 1")
# print("------------------------")
# m = HashMap(11, hash_function_2)
# for i in range(1, 6):
#     m.put(str(i), str(i * 10))
# print(m.get_keys_and_values())
#
# m.resize_table(2)
# print(m.get_keys_and_values())
#
# m.put('20', '200')
# m.remove('1')
# m.resize_table(12)
# print(m.get_keys_and_values())
#
# print("\nPDF - __iter__(), __next__() example 1")
# print("---------------------")
# m = HashMap(10, hash_function_1)
# for i in range(5):
#     m.put(str(i), str(i * 10))
# print(m)
# for item in m:
#     print('K:', item.key, 'V:', item.value)
#
# print("\nPDF - __iter__(), __next__() example 2")
# print("---------------------")
# m = HashMap(10, hash_function_2)
# for i in range(5):
#     m.put(str(i), str(i * 24))
# m.remove('0')
# m.remove('4')
# print(m)
# for item in m:
#     print('K:', item.key, 'V:', item.value)

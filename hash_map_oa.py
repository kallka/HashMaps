# Name: Karina Kallas
# OSU Email: kallask@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/22
# Description: Implement a HashMap class that uses a dynamic array to store the hash table and implements
#              Open Addressing with Quadratic Probing for collision resolution inside the dynamic array.
#              Key/Value pairs are stored in the array.


from a6_include import *


class HashEntry:

    def __init__(self, key: str, value: object):
        """
        Initializes an entry for use in a hash map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.key = key
        self.value = value
        self.is_tombstone = False

    def __str__(self):
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return f"K: {self.key} V: {self.value} TS: {self.is_tombstone}"


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash, index = 0, 0
    index = 0
    for letter in key:
        hash += (index + 1) * ord(letter)
        index += 1
    return hash


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses Quadratic Probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()

        for _ in range(capacity):
            self.buckets.append(None)

        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            out += str(i) + ': ' + str(self.buckets[i]) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(None)
        self.size = 0

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key. If the key is not in the hash map,
        method returns None.
        """
        if self.size == 0:
            return None
        else:
            index = self.hash_function(key)
            hash_obj = self.help_find(index, key)
            if hash_obj[1]:
                return hash_obj[1].value
            else:
                return None


    def help_find(self, index, new_key, search=None):
        """Method helps find the correct index and object based on a given key."""
        # is index out or range?:
        if index >= self.capacity:
            index = index % self.capacity
        #save first index:
        initial_index = index

        # index is in range; is there something at the index?:
        cur_obj = self.buckets.get_at_index(index)
        j = 1
        while cur_obj:
            if cur_obj.is_tombstone is True and search is None:
                return index, cur_obj
            if cur_obj.key == new_key:
                return index, cur_obj
            # Try next index:
            index = (initial_index + j ** 2)
            if index >= self.capacity:
                index = index % self.capacity
            j += 1
            cur_obj = self.buckets.get_at_index(index)
        # hit an empty index; return index and None:
        return index, None

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair in the hash map. If the given key already exists in the hash map,
        its associated value is replaced with the new value. If the given key is not in the hash map, a key/value
        pair is added.
        """
        # check resize before adding a key/value pair:
        if self.table_load() >= 1/2:
            self.resize_table(self.capacity*2)
        # create a hash entry and send key through function to determine start index:
        new_object = HashEntry(key, value)
        index = self.hash_function(key)

        # Send index to help_find to determine if quadratic probing needed or if something at index:
        # Save index and old_obj for code legibility:
        insert_spot = self.help_find(index, key)
        index = insert_spot[0]
        old_obj = insert_spot[1]
        # Is old_obj a tombstone?; Is old_obj None?; Does old_obj.key match new key?:
        if old_obj is None:
            self.buckets.set_at_index(index, new_object)
            self.size += 1
        elif old_obj.is_tombstone is True:
            self.buckets.set_at_index(index, new_object)
            self.size += 1
        elif old_obj.key == key:
            old_obj.value = value


    def remove(self, key: str) -> None:
        """
        Method removes a given key and its value from the hash map. Nothing is returned.
        """
        if self.size == 0:
            return
        else:
            index = self.hash_function(key)
            hash_obj = self.help_find(index, key, True)
            if hash_obj[1] and hash_obj[1].is_tombstone is False:
                remove_obj = hash_obj[1]
                remove_obj.is_tombstone = True
                self.size -= 1
            else:
                return

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if given key is in the hash map. Otherwise, it returns False
        """
        if self.size == 0:
            return False
        else:
            index = self.hash_function(key)
            hash_obj = self.help_find(index, key, True)
            if hash_obj[1] and hash_obj[1].is_tombstone is False:
                return True
            else:
                return False

    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the hash table.
        """
        return self.capacity - self.size

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        return self.size/self.capacity

    def resize_table(self, new_capacity: int) -> None:
        """
        Method cahnges the capacity of the internal hash table. All key/value pairs must remain
        in the new hash map; all hash table links must be rehashed. If new capacity is < 1, or less
        than current number of elements, the method does nothing.
        """
        if new_capacity < 1 or new_capacity < self.size:
            return
        else:
            # save values:
            save_buckets = self.buckets
            old_capacity = self.capacity
            # create new Dynamic Array:
            self.size = 0
            self.buckets = DynamicArray()
            for _ in range(new_capacity):
                self.buckets.append(None)
            self.capacity = new_capacity
            #rehash old keys:
            for num in range(old_capacity):
                hash_obj = save_buckets.get_at_index(num)
                if hash_obj and hash_obj.is_tombstone is False:
                    self.put(hash_obj.key, hash_obj.value)

    def get_keys(self) -> DynamicArray:
        """
        Method returns a Dynamic Array that contains all keys stored in the hash map.
        The order of the keys does not matter.
        """
        new_array = DynamicArray()
        for num in range(self.capacity):
            hash_obj = self.buckets.get_at_index(num)
            if hash_obj and hash_obj.is_tombstone is False:
                new_array.append(hash_obj.key)
        return new_array


if __name__ == "__main__":

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 10)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key2', 20)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key1', 30)
    print(m.empty_buckets(), m.size, m.capacity)
    m.put('key4', 40)
    print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    # this test assumes that put() has already been correctly implemented
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.size, m.capacity)

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.size, m.capacity)

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.size, m.capacity)
    m.put('key1', 10)
    print(m.size, m.capacity)
    m.put('key2', 20)
    print(m.size, m.capacity)
    m.resize_table(100)
    print(m.size, m.capacity)
    m.clear()
    print(m.size, m.capacity)

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.size, m.capacity)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.size, m.capacity)
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.size, m.capacity, m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.size, m.capacity)

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            result &= m.contains_key(str(key))
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.size, m.capacity, round(m.table_load(), 2))

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

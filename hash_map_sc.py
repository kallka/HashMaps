# Name: Karina Kallas
# OSU Email: kallask@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 3/11/22
# Description: Implement a Hash Map using a Dynamic Array to store the hash table and
#              a Linked List (singly linked) to implement chaining for collision resolution.
#              Each key-value pair is stored in an SL Node (singly linked).


from a6_include import *


def hash_function_1(key: str) -> int:
    """
    Sample Hash function #1 to be used with A5 HashMap implementation
    DO NOT CHANGE THIS FUNCTION IN ANY WAY
    """
    hash = 0
    for letter in key:
        hash += ord(letter)
    return hash


def hash_function_2(key: str) -> int:
    """
    Sample Hash function #2 to be used with A5 HashMap implementation
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
        Init new HashMap based on DA with SLL for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.buckets = DynamicArray()
        for _ in range(capacity):
            self.buckets.append(LinkedList())
        self.capacity = capacity
        self.hash_function = function
        self.size = 0

    def __str__(self) -> str:
        """
        Overrides object's string method
        Return content of hash map t in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self.buckets.length()):
            list = self.buckets.get_at_index(i)
            out += str(i) + ': ' + str(list) + '\n'
        return out

    def clear(self) -> None:
        """
        Method clears the contents of the hash map. It does not change the underlying hash table capacity.
        """
        self.buckets = DynamicArray()
        for _ in range(self.capacity):
            self.buckets.append(LinkedList())
        self.size = 0

    def get(self, key: str) -> object:
        """
        Method returns the value associated with the given key. If the key is not in the hash map, return None.
        """
        linked_list = self.find_ll(key)
        node = linked_list.contains(key)
        if node:
            return node.value
        else:
            return None

    def find_ll(self, key):
        """
        Helper method takes a key, sends it through the hash function, and returns the linked list that
        corresponds to the correct location.
        """
        index = self.hash_function(key)
        if index >= self.capacity:
            index = index % self.capacity
        linked_list = self.buckets.get_at_index(index)
        return linked_list

    def put(self, key: str, value: object) -> None:
        """
        Method updates the key/value pair in the hash map. If the given key already exists in the
        hash map, its associated value is replaced with the new value. If the given key is not
        in the hash map, the key/value pair is added.
        """
        linked_list = self.find_ll(key)
        # if the indexed bucket is empty:
        if linked_list.length() == 0:
            linked_list.insert(key, value)    # order is (key, value)
            self.size += 1
        # if nodes in linked list:
        else:
            # key is in linked list; change the value:
            if self.contains_key(key):
                node = linked_list.contains(key)
                node.value = value
                return
            # key is not in linked list; add the node:
            else:
                linked_list.insert(key, value)
                self.size += 1


    def remove(self, key: str) -> None:
        """
        Method removes the given key and its associated value from the hash map.
        If the key is not in the hash map, it does nothing.
        """
        linked_list = self.find_ll(key)
        if linked_list.contains(key):
            linked_list.remove(key)
            self.size -= 1
        else:
            return

    def contains_key(self, key: str) -> bool:
        """
        Method returns True if the given key is in the hash map. Otherwise, it returns False.
        """
        if self.size == 0:
            return False
        else:
            linked_list = self.find_ll(key)
            if linked_list.length() == 0:
                return False
            elif linked_list.contains(key):
                return True
            else:
                return False


    def empty_buckets(self) -> int:
        """
        Method returns the number of empty buckets in the hash table.
        """
        count = 0
        for num in range(self.capacity):
            if self.buckets.get_at_index(num).length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        Method returns the current hash table load factor.
        """
        n = self.size
        m = self.capacity
        return n/m

    def resize_table(self, new_capacity: int) -> None:
        """
        Method changes the capacity of the internal hash table. All existing key/value pairs remain
        in the new hash map. All hash table links are rehashed. If new_capacity is < 1, nothing is done.
        """
        if new_capacity < 1:
            return
        else:
            # save old buckets and old capacity; create new hash map:
            save_buckets = self.buckets
            old_capacity = self.capacity
            self.buckets = DynamicArray()
            self.size = 0
            self.capacity = new_capacity
            for num in range(new_capacity):
                self.buckets.append(LinkedList())
            # rehash the old table links:
            for num in range(old_capacity):
                linked_list = save_buckets.get_at_index(num)
                if linked_list.length() > 0:
                    node = linked_list.head
                    while node is not None:
                        self.put(node.key, node.value)
                        node = node.next

    def get_keys(self) -> DynamicArray:
        """
        Method returns a Dynamic Array that contains all keys stored in the hash map.
        The order of keys in the Dynamic Array does not matter.
        """
        new_array = DynamicArray()
        for num in range(self.capacity):
            linked_list = self.buckets.get_at_index(num)
            if linked_list.length() > 0:
                node = linked_list.head
                while node is not None:
                    new_array.append(node.key)
                    node = node.next
        return new_array



# BASIC TESTING
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

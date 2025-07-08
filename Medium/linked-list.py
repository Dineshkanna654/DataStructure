class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last_node = self.head
        while last_node.next:
            last_node = last_node.next
        last_node.next = new_node

    def display(self):
        current_node = self.head
        print(current_node)
        while current_node:
            # print(current_node.data, end=" -> ")
            # print(current_node.next, end=" -> ")
            current_node = current_node.next
        print("None")

# Example usage
ll = LinkedList()
ll.append(1)
ll.append(2)
ll.append(3)
ll.display()  # Output: 1 -> 2 -> 3 -> None
# This code defines a simple linked list with methods to append data and display the list.
# It can be used to create a linked list of any data type, similar to how the Car class can be used to create car objects with specific attributes.
# The linked list can be extended with more methods like insert, delete, or search as needed
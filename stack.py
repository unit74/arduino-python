class Stack:
    def __init__(self):
        self.items = []

    def isEmpty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def peek(self):
        return self.items[len(self.items)-1]

    def size(self):
        return len(self.items)

    def print(self):
        print("----go_list----")
        for i in range(len(self.items)):
            print(self.items[len(self.items) - i - 1])
        print("----------\n")
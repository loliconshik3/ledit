import random

class Test:
	
    def __init__(self):
		
        self.random = random.randint(1, 100)
		
    def print_random(self):
		
        print(self.random)

    def reset_random(self):
        
        self.random = random.randint(1, 100)


test_everywhere=True

test = Test()
test.print_random()
test.reset_random()
test.print_random()

input()


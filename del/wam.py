import random

def generate_random_data(num_entries):
    data = []
    for _ in range(num_entries):
        name_length = random.randint(5, 10)
        name = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(name_length))
        age = random.randint(18, 80)
        data.append(f"{name},{age}")
    return data

random_data = generate_random_data(30)
for entry in random_data:
    print(entry)

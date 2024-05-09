import random
import string

def generate_random_name(length=6):
    """Generate a random name."""
    return ''.join(random.choices(string.ascii_uppercase, k=length))

# Generate random scores with random names
num_scores = 10  # Number of scores to generate
min_score = 10   # Minimum score
max_score = 20   # Maximum score

# Generate and print random scores
for _ in range(num_scores):
    name = generate_random_name()
    score = random.randint(min_score, max_score)
    print(f"{name},{score}")

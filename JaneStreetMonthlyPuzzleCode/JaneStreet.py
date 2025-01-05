from itertools import combinations

def get_next_sequence(nums):
    """Calculate next sequence by taking absolute differences between adjacent numbers"""
    return tuple(abs(nums[i] - nums[(i+1)%4]) for i in range(4))

def count_steps_to_zero(nums):
    """Count steps until sequence becomes all zeros"""
    seen = {nums}  # Track seen sequences to detect cycles
    steps = 1
    
    while any(nums):  # While not all zeros
        nums = get_next_sequence(nums)
        steps += 1
        if nums in seen:  # If we hit a cycle, this sequence never reaches zero
            return 0
        seen.add(nums)
    return steps

def find_optimal_sequence(target):
    """Find sequence with maximum steps to zero and minimum sum of middle values"""
    max_steps = 1
    min_sum = float('inf')
    best_pairs = []
    
    # Only need to check up to target/2 for middle values since abs(differences) will be the same
    for a, b in combinations(range(target//2 + 1), 2):
        sequence = (0, a, b, target)
        steps = count_steps_to_zero(sequence)
        
        if steps > max_steps:
            max_steps = steps
            min_sum = a + b
            best_pairs = [(a, b)]
        elif steps == max_steps:
            curr_sum = a + b
            if curr_sum < min_sum:
                min_sum = curr_sum
                best_pairs = [(a, b)]
            elif curr_sum == min_sum:
                best_pairs.append((a, b))
                
    return max_steps, best_pairs, min_sum

# Test specific value
target = 8646064
steps, pairs, min_sum = find_optimal_sequence(target)
if steps > 20:
    print(f"{target}: {steps} {pairs}")

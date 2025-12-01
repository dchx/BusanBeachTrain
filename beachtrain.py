'''
There is a railway with seven stations: A, B, C, D, E, F, G. The terminal stations are A and G. There are trains in both directions that stop at every station. A pass ticket allows boarding at each of the seven stations exactly once. At all stations excluding the terminals, passengers may ride in either direction. They may disembark at any station, but all passengers must exit when the train reaches terminal stations A or G. We define the segment of railway between any two adjacent stations as a section. If I purchase this pass ticket, how should I travel to maximize the number of sections I traverse? Repeated sections count toward the total. In this travel plan, I may walk from one station to another after disembarking, but each walk is limited to a maximum of x sections. If multiple plans yield the maximum number of traversed sections, select the one with the minimum number of total walking sections. Please write a python code to choose the optimal travel plan and compute the maximum number of traversed sections for x = 0, 1, 2, 3.
Author: Gemini 2.5 Pro
'''
import functools

# --- global constants definition ---
STATIONS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
STATIONS = {'(A) Mipo': 0, '(B) Dalmaji Tunnel': 1, '(C) Haeworl Skywalk': 2, '(D) Cheongsapo': 3, '(E) Daritdol Skywalk': 4, '(F) Gudeokpo': 5, '(G) Songjeong': 6}
STATION_NAMES = {v: k for k, v in STATIONS.items()}
NUM_STATIONS = len(STATIONS)

# --- core solution function ---

@functools.lru_cache(maxsize=None)
def find_best_path_recursive(current_loc, used_mask, x):
    """
    Recursive function used to find the optimal path starting from
    the current location.
    Use lru_cache for memoization to avoid redundant computations.

    Args:
        current_loc (int): index of current station
        used_mask (int): A bitmask indicating what stations have been used to board
        x (int): Maximum number of walking sections allowed per trip

    Returns:
        tuple: (Maximum traversed sections, minimum walking sections, optimal route)
    """
    # Basis situation: All tickets have been used. The journey has ended.
    if used_mask == (1 << NUM_STATIONS) - 1:
        return 0, 0, []

    best_total_travel = -1
    best_total_walk = float('inf')
    best_path = []

    # Iterate through all unused stations as the next boarding station.
    for boarding_idx in range(NUM_STATIONS):
        # Check whether this station has been used yet.
        if not (used_mask & (1 << boarding_idx)):
            walk_dist = abs(current_loc - boarding_idx)

            # Check whether the walking distance is within the permitted range.
            if walk_dist <= x:
                # Traverse all possible disembark stations
                for alight_idx in range(NUM_STATIONS):
                    if alight_idx == boarding_idx:
                        continue  # must move at least one interval

                    # Verify the validity of the travel direction
                    is_valid_ride = False
                    # Rule 1: At intermediate stations (B–F), you may proceed to any other station.
                    if 1 <= boarding_idx <= NUM_STATIONS - 2:
                        is_valid_ride = True
                    # Rule 2: At the terminal station A, you must proceed toward G.
                    elif boarding_idx == 0 and alight_idx > boarding_idx:
                        is_valid_ride = True
                    # Rule 3: At the terminal station G, you must proceed toward A.
                    elif boarding_idx == NUM_STATIONS - 1 and alight_idx < boarding_idx:
                        is_valid_ride = True

                    if is_valid_ride:
                        travel_dist = abs(boarding_idx - alight_idx)
                        new_mask = used_mask | (1 << boarding_idx)

                        # Recursive call to find the optimal route for the subsequent journey
                        future_travel, future_walk, future_path = find_best_path_recursive(alight_idx, new_mask, x)

                        # If the subsequent path is valid (i.e., it does not get stuck)
                        if future_travel != -1:
                            current_total_travel = travel_dist + future_travel
                            current_total_walk = walk_dist + future_walk

                            # Compare and update the best results
                            # Primary goal: Maximize the riding distance
                            if current_total_travel > best_total_travel:
                                best_total_travel = current_total_travel
                                best_total_walk = current_total_walk
                                current_step = [{'walk_from': current_loc, 'walk_to': boarding_idx, 'board': boarding_idx, 'alight': alight_idx}]
                                best_path = current_step + future_path
                            # Secondary goal: Minimize walking distance when the riding distances are the same.
                            elif current_total_travel == best_total_travel and current_total_walk < best_total_walk:
                                best_total_walk = current_total_walk
                                current_step = [{'walk_from': current_loc, 'walk_to': boarding_idx, 'board': boarding_idx, 'alight': alight_idx}]
                                best_path = current_step + future_path

    return best_total_travel, best_total_walk, best_path

def solve_for_x(x):
    """
    Calculate and return the optimal solution for a given x value.
    This function handles the start of the journey, as the first step has no preceding walk.
    """
    find_best_path_recursive.cache_clear()  # Reset the cache for each x

    overall_best_travel = -1
    overall_best_walk = float('inf')
    overall_best_path = []

    # Traverse all possible first boarding stations
    for first_boarding_idx in range(NUM_STATIONS):
        # Traverse all possible first disembark stations
        for first_alight_idx in range(NUM_STATIONS):
            if first_alight_idx == first_boarding_idx:
                continue

            is_valid_ride = False
            if 1 <= first_boarding_idx <= NUM_STATIONS - 2:
                is_valid_ride = True
            elif first_boarding_idx == 0 and first_alight_idx > first_boarding_idx:
                is_valid_ride = True
            elif first_boarding_idx == NUM_STATIONS - 1 and first_alight_idx < first_boarding_idx:
                is_valid_ride = True

            if is_valid_ride:
                first_travel = abs(first_boarding_idx - first_alight_idx)
                first_mask = (1 << first_boarding_idx)
                
                future_travel, future_walk, future_path = find_best_path_recursive(first_alight_idx, first_mask, x)
                
                if future_travel != -1:
                    total_travel = first_travel + future_travel
                    total_walk = 0 + future_walk  # The journey begins without walking.

                    if total_travel > overall_best_travel:
                        overall_best_travel = total_travel
                        overall_best_walk = total_walk
                        first_step = [{'walk_from': 'Start', 'walk_to': first_boarding_idx, 'board': first_boarding_idx, 'alight': first_alight_idx}]
                        overall_best_path = first_step + future_path
                    elif total_travel == overall_best_travel and total_walk < overall_best_walk:
                        overall_best_walk = total_walk
                        first_step = [{'walk_from': 'Start', 'walk_to': first_boarding_idx, 'board': first_boarding_idx, 'alight': first_alight_idx}]
                        overall_best_path = first_step + future_path
                        
    return overall_best_travel, overall_best_walk, overall_best_path

def print_solution(x, travel, walk, path):
    """
    Format and print the best solution found.
    """
    print(f"When x = {x} (at most {x} sections of each walk):")
    if travel == -1:
        print("  No valid travel itinerary found.")
        return
        
    print(f"  Best result: Maximum number of riding sections = {travel}, Minimum number of walking sections = {walk}")
    print("  Plan details:")
    
    cumulative_travel = 0
    cumulative_walk = 0
    
    for i, step in enumerate(path):
        walk_dist = abs(step['walk_to'] - step['walk_from']) if step['walk_from'] != 'Start' else 0
        travel_dist = abs(step['alight'] - step['board'])
        
        cumulative_travel += travel_dist
        cumulative_walk += walk_dist
        
        # Construct descriptive string
        desc = f"    Step {i+1}: "
        if step['walk_from'] != 'Start' and walk_dist > 0:
            desc += f"Walk from {STATION_NAMES[step['walk_from']]} for {walk_dist} sections to {STATION_NAMES[step['walk_to']]}. Then, "
        
        desc += f"Board at {STATION_NAMES[step['board']]}, ride for {travel_dist} sections and disembark at {STATION_NAMES[step['alight']]}."
        
        print(desc)
        print(f"           (Cumulative ride: {cumulative_travel}, Cumulative walk: {cumulative_walk})")
    print("-" * 50)

# --- main program ---
if __name__ == "__main__":
    print("Start solving the railway travel optimization problem...")
    print("=" * 50)
    for x_val in range(4):
        best_travel, best_walk, best_path = solve_for_x(x_val)
        print_solution(x_val, best_travel, best_walk, best_path)

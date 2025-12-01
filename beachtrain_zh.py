'''
有一条铁路，上面有七座火车站，依次是ABCDEFG。在两头的A和G站是终点站。这条铁路的两个方向都有站站停的列车。这条铁路有一个套票，这个套票在可以在全线7个车站分别上且只上一次车。除了终点站，在某个车站上车后可以乘坐任意方向的列车。上车后可以在任意车站下车，但是列车抵达两端的终点站A和G时全部乘客都要下车。我们把相邻两站之间的一段路叫做一个区间。如果我买了这个套票，要怎么乘坐才能使得我乘坐过的区间数最大？重复乘坐的区间要累计统计。在这个乘坐方案中，我在一座车站下车后也可以步行到另一座车站上车，但每次最多步行x个区间。如果有多个乘坐区间数最大的方案，要选取总步行区间数最小的那个。请写一个python程序，分别计算x = 0, 1, 2, 3时的最佳乘坐方案和最大乘坐区间数。
Author: Gemini 2.5 Pro
'''
import functools

# --- 全局常量定义 ---
STATIONS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4, 'F': 5, 'G': 6}
STATIONS = {'(A) 尾浦': 0, '(B) 迎月隧道': 1, '(C) 海月瞭望台': 2, '(D) 青沙浦': 3, '(E) 桥石展望台': 4, '(F) 九德浦': 5, '(G) 松亭': 6}
STATION_NAMES = {v: k for k, v in STATIONS.items()}
NUM_STATIONS = len(STATIONS)

# --- 核心求解函数 ---

@functools.lru_cache(maxsize=None)
def find_best_path_recursive(current_loc, used_mask, x):
    """
    递归函数，用于寻找从当前状态出发的最佳路径。
    使用 lru_cache 进行记忆化，避免重复计算。

    Args:
        current_loc (int): 当前所在的车站编号。
        used_mask (int): 一个位掩码，表示哪些车站的上车票已被使用。
        x (int): 单次允许的最大步行区间数。

    Returns:
        tuple: (最大乘坐区间, 最小步行区间, 最佳路径列表)
    """
    # 基本情况：所有车票都已使用，旅程结束
    if used_mask == (1 << NUM_STATIONS) - 1:
        return 0, 0, []

    best_total_travel = -1
    best_total_walk = float('inf')
    best_path = []

    # 遍历所有未使用的车票，作为下一次上车的车站
    for boarding_idx in range(NUM_STATIONS):
        # 检查这张票是否尚未使用
        if not (used_mask & (1 << boarding_idx)):
            walk_dist = abs(current_loc - boarding_idx)

            # 检查步行距离是否在允许范围内
            if walk_dist <= x:
                # 遍历所有可能的下车点
                for alight_idx in range(NUM_STATIONS):
                    if alight_idx == boarding_idx:
                        continue  # 必须移动至少一个区间

                    # 验证乘车方向的有效性
                    is_valid_ride = False
                    # 规则 1: 在中间站 (B-F)，可以去任何其他车站
                    if 1 <= boarding_idx <= NUM_STATIONS - 2:
                        is_valid_ride = True
                    # 规则 2: 在始发站 A，必须向 G 的方向走
                    elif boarding_idx == 0 and alight_idx > boarding_idx:
                        is_valid_ride = True
                    # 规则 3: 在终点站 G，必须向 A 的方向走
                    elif boarding_idx == NUM_STATIONS - 1 and alight_idx < boarding_idx:
                        is_valid_ride = True

                    if is_valid_ride:
                        travel_dist = abs(boarding_idx - alight_idx)
                        new_mask = used_mask | (1 << boarding_idx)

                        # 递归调用，寻找后续旅程的最佳方案
                        future_travel, future_walk, future_path = find_best_path_recursive(alight_idx, new_mask, x)

                        # 如果后续路径有效（即没有卡住）
                        if future_travel != -1:
                            current_total_travel = travel_dist + future_travel
                            current_total_walk = walk_dist + future_walk

                            # 比较并更新最佳结果
                            # 主要目标：最大化乘坐区间
                            if current_total_travel > best_total_travel:
                                best_total_travel = current_total_travel
                                best_total_walk = current_total_walk
                                current_step = [{'walk_from': current_loc, 'walk_to': boarding_idx, 'board': boarding_idx, 'alight': alight_idx}]
                                best_path = current_step + future_path
                            # 次要目标：在乘坐区间相同时，最小化步行区间
                            elif current_total_travel == best_total_travel and current_total_walk < best_total_walk:
                                best_total_walk = current_total_walk
                                current_step = [{'walk_from': current_loc, 'walk_to': boarding_idx, 'board': boarding_idx, 'alight': alight_idx}]
                                best_path = current_step + future_path

    return best_total_travel, best_total_walk, best_path

def solve_for_x(x):
    """
    为给定的 x 值计算并返回最终的最佳方案。
    这个函数处理旅程的开始，因为第一步没有前置的步行。
    """
    find_best_path_recursive.cache_clear()  # 为每个 x 重置缓存

    overall_best_travel = -1
    overall_best_walk = float('inf')
    overall_best_path = []

    # 遍历所有可能的第一次上车站
    for first_boarding_idx in range(NUM_STATIONS):
        # 遍历所有可能的第一次下车站
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
                    total_walk = 0 + future_walk  # 旅程开始时没有步行

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
    格式化并打印找到的最佳方案。
    """
    print(f"当 x = {x} (每次最多步行 {x} 个区间) 时:")
    if travel == -1:
        print("  未找到有效的旅行方案。")
        return
        
    print(f"  最佳结果: 最大乘坐区间数 = {travel}, 最小总步行区间数 = {walk}")
    print("  方案详情:")
    
    cumulative_travel = 0
    cumulative_walk = 0
    
    for i, step in enumerate(path):
        walk_dist = abs(step['walk_to'] - step['walk_from']) if step['walk_from'] != 'Start' else 0
        travel_dist = abs(step['alight'] - step['board'])
        
        cumulative_travel += travel_dist
        cumulative_walk += walk_dist
        
        # 构建描述字符串
        desc = f"    第 {i+1} 步: "
        if step['walk_from'] != 'Start' and walk_dist > 0:
            desc += f"从 {STATION_NAMES[step['walk_from']]} 步行 {walk_dist} 个区间到 {STATION_NAMES[step['walk_to']]}。然后，"
        
        desc += f"从 {STATION_NAMES[step['board']]} 上车, 乘坐 {travel_dist} 个区间后在 {STATION_NAMES[step['alight']]} 下车。"
        
        print(desc)
        print(f"           (累计乘坐: {cumulative_travel}, 累计步行: {cumulative_walk})")
    print("-" * 50)

# --- 主程序入口 ---
if __name__ == "__main__":
    print("开始计算铁路旅行优化问题...")
    print("=" * 50)
    for x_val in range(4):
        best_travel, best_walk, best_path = solve_for_x(x_val)
        print_solution(x_val, best_travel, best_walk, best_path)

import random
from engine.performance import PerformanceTracker

# --- CÁC HÀM PHỤ TRỢ ĐÃ ĐƯỢC CHUẨN HÓA ---

def H_match(state, solution):
    """Tính heuristic - số quân đặt SAI vị trí (càng nhỏ càng tốt)."""
    return sum(1 for i in range(len(state)) if state[i] != solution[i])

def fitness(state, solution):
    """Hàm fitness"""
    # Fitness = số quân đặt đúng. 
    return len(state) - H_match(state, solution)

def Init_population(size, n):
    """Khởi tạo quần thể: size cá thể, mỗi cá thể là 1 hoán vị của 0..n-1"""
    return [random.sample(range(n), n) for _ in range(size)]

def Tournament_selection(population, fitnesses, k=3):
    """Dùng fitnesses đã được tính toán sẵn để tăng hiệu quả."""
    # Lấy ngẫu nhiên k chỉ số từ quần thể
    indices = random.sample(range(len(population)), k)
    
    # Tìm index của cá thể có fitness cao nhất trong nhóm được chọn
    best_local_idx = max(indices, key=lambda i: fitnesses[i])
    
    return population[best_local_idx]

def Order_crossover(p1, p2):
    """Order Crossover (OX) cho bài toán hoán vị."""
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))
    child = [None] * n
    child[a:b+1] = p1[a:b+1]
    pos = (b+1) % n
    for gene in p2:
        if gene not in child:
            child[pos] = gene
            pos = (pos + 1) % n
    return child

def Mutate(ind, mutation_rate=0.1):
    """Đột biến bằng cách hoán đổi 2 vị trí ngẫu nhiên."""
    new_ind = ind[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(ind)), 2)
        new_ind[i], new_ind[j] = new_ind[j], new_ind[i]
    return new_ind


def GeneticAlgorithm(solution, population_size=30, generations=500, mutation_rate=0.2, crossover_rate=0.9, mode="goal"):
    """
    Genetic Algorithm cho 8 Rooks
    """
    n = len(solution)
    tracker = PerformanceTracker("Genetic Algorithm")
    tracker.start()

    # Khởi tạo quần thể và tính fitness ban đầu
    population = Init_population(population_size, n)
    fitnesses = [fitness(ind, solution) for ind in population]
    
    # Tìm cá thể tốt nhất trong quần thể ngẫu nhiên ban đầu
    best_idx_initial = max(range(len(population)), key=lambda i: fitnesses[i])
    overall_best_individual = population[best_idx_initial]
    overall_best_fitness = fitnesses[best_idx_initial]

    # Khởi tạo "Lịch sử Cải tiến" cho visualization với điểm xuất phát
    path_to_solution = [overall_best_individual.copy()] if mode == "all" else None
    
    # Bắt đầu quá trình tiến hóa
    for gen in range(generations):
        tracker.add_node(population_size)
        
        #Sinh thế hệ mới
        new_population = []
        
        #Giữ lại 1 cá thể tốt nhất từ trước đến nay
        if overall_best_individual:
            new_population.append(overall_best_individual.copy())
        
        while len(new_population) < population_size:
            # Lựa chọn cha mẹ
            p1 = Tournament_selection(population, fitnesses)
            p2 = Tournament_selection(population, fitnesses)

            # Lai ghép có điều kiện
            if random.random() < crossover_rate:
                child = Order_crossover(p1, p2)
            else:
                child = p1[:] # Sao chép một cha mẹ nếu không lai ghép

            # Đột biến
            child = Mutate(child, mutation_rate)
            new_population.append(child)
        
        population = new_population
        fitnesses = [fitness(ind, solution) for ind in population]

        # Tìm cá thể tốt nhất trong thế hệ mới
        best_idx_current_gen = max(range(len(population)), key=lambda i: fitnesses[i])
        current_best_fitness = fitnesses[best_idx_current_gen]

        # Cập nhật cá thể tốt nhất nếu có sự cải tiến
        if current_best_fitness > overall_best_fitness:
            overall_best_fitness = current_best_fitness
            overall_best_individual = population[best_idx_current_gen]
            
            if mode == "all":
                # Chỉ ghi lại vào "đường đi" khi có sự cải tiến
                path_to_solution.append(overall_best_individual.copy())
        
        # Kiểm tra điều kiện dừng nếu đã tìm thấy lời giải hoàn hảo (fitness = 8)
        if overall_best_fitness == n:
            tracker.goal_found()
            break 

    tracker.stop()
    
    if mode == "all":
        return path_to_solution, tracker.get_stats()
    else: 
        if overall_best_fitness == n:
             tracker.goal_found() 
        return overall_best_individual, tracker.get_stats()
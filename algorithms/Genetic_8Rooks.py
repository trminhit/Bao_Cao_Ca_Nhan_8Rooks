import random

def H_match(state, solution):
    """Tính fitness: số quân đặt đúng vị trí"""
    return sum(1 for i in range(len(state)) if state[i] == solution[i])

def Init_population(size, n):
    """Khởi tạo quần thể: size cá thể, mỗi cá thể là 1 hoán vị của 0..n-1"""
    return [random.sample(range(n), n) for _ in range(size)]

def Tournament_selection(population, fitnesses, k=3):
    """
    - Lấy ngẫu nhiên k cá thể từ quần thể
    - Trả về cá thể có fitness cao nhất trong số đó
    """
    selected = random.sample(list(zip(population, fitnesses)), k)
    selected.sort(key=lambda x: x[1], reverse=True)
    return selected[0][0]

def Order_crossover(p1, p2):
    """
    Order Crossover (OX) cho hoán vị:
    - Chọn ngẫu nhiên 1 đoạn từ p1
    - Copy nguyên đoạn này vào con
    - Điền các gene còn lại theo thứ tự xuất hiện trong p2
    """
    n = len(p1)
    a, b = sorted(random.sample(range(n), 2))   # chọn đoạn [a..b]
    child = [None] * n

    # copy đoạn từ p1
    child[a:b+1] = p1[a:b+1]

    # điền phần còn lại từ p2
    pos = (b+1) % n
    for gene in p2:
        if gene not in child:   # chỉ chèn gene chưa có trong child
            child[pos] = gene
            pos = (pos + 1) % n

    return child

def Mutate(ind, mutation_rate=0.1):
    """
    Đột biến:
    - Với xác suất mutation_rate, chọn 2 vị trí ngẫu nhiên
    - Hoán đổi chúng để duy trì tính hoán vị
    """
    new_ind = ind[:]
    if random.random() < mutation_rate:
        i, j = random.sample(range(len(ind)), 2)
        new_ind[i], new_ind[j] = new_ind[j], new_ind[i]
    return new_ind

def GeneticAlgorithm(solution, population_size=50, generations=500, mutation_rate=0.1):
    """
    Genetic Algorithm 
    - population_size: số cá thể trong quần thể
    - generations: số thế hệ tối đa
    - mutation_rate: xác suất đột biến
    """
    n = len(solution)
    #Khởi tạo quần thể ban đầu
    population = Init_population(population_size, n)
    path = []   # lưu lại best qua từng thế hệ

    for gen in range(generations):
        # Đánh giá fitness của toàn bộ quần thể
        fitnesses = [H_match(ind, solution) for ind in population]

        # Tìm cá thể tốt nhất 
        best_idx = max(range(len(population)), key=lambda i: fitnesses[i])
        best = population[best_idx]
        best_fit = fitnesses[best_idx]
        path.append(best)

        # Nếu tìm thấy nghiệm tối ưu 
        if best_fit == n:
            return path

        # Sinh thế hệ mới
        new_population = [best]   # elitism: giữ lại best
        while len(new_population) < population_size: #cho tới khi đủ 50 con
            # chọn cha mẹ bằng tournament
            p1 = Tournament_selection(population, fitnesses)
            p2 = Tournament_selection(population, fitnesses)

            # lai ghép (tạo con)
            child = Order_crossover(p1, p2)

            # đột biến (nếu xảy ra)
            child = Mutate(child, mutation_rate)

            new_population.append(child)

        # cập nhật quần thể
        population = new_population

    return path

import pygame

# Board constants
BOARD_OFFSET_X = 400
BOARD_OFFSET_Y = 80
RIGHT_SIDE_PANEL_WIDTH = 180
LEGEND_HEIGHT = 210
STATS_HEIGHT = 380
SMALL_CELL_SIZE = 37

# Colors 
WHITE = (255, 255, 255) 

PASTEL_BG = (230, 240, 245)           # Nền chính (
PASTEL_ACCENT = (100,130,180)        # Màu nhấn/lựa chọn (Vibrant Sky Blue)
PASTEL_DARK_TEXT = (40, 60, 80)       # Chữ chính, tiêu đề (Charcoal Blue)

PASTEL_MEDIUM_TEXT = (80, 100, 120)   # Chữ phụ, mô tả 
PASTEL_LIGHT_BORDER = (160, 200, 210) # Đường viền, phân cách 
DISABLED_BG = (220, 220, 220)         # Nền nút thụ động (Light Gray)
DISABLED_TEXT = (150, 150, 150)       # Chữ nút thụ động (Medium Gray)
PASTEL_LIGHT_TEXT_ON_ACCENT = (200, 220, 230)

# Màu bàn cờ pastel
BOARD_LIGHT_CELL = (245, 245, 245) 
BOARD_DARK_CELL = (160, 195, 215)  


class Renderer:
    def __init__(self, screen, game, rook_img):
        self.game = game
        self.screen = screen
        self.rook_img = pygame.transform.scale(rook_img, (SMALL_CELL_SIZE, SMALL_CELL_SIZE))
        
        self.font = pygame.font.SysFont("segoeui", 18)
        self.title_font = pygame.font.SysFont("segoeui", 28, bold=True)
        self.small_font = pygame.font.SysFont("segoeui", 16)

        self.GROUP_BUTTON_WIDTH = 180
        self.GROUP_BUTTON_HEIGHT = 50
        self.ALG_BUTTON_WIDTH = 250
        self.ALG_BUTTON_HEIGHT = 60
        self.BUTTON_SPACING = 5
        self.BUTTON_RADIUS = 8

        self.algorithm_groups = [
            {
                "name": "Uninformed Search",
                "algorithms": [
                    {"name": "BFS", "desc": "Breadth-First Search"},
                    {"name": "DFS", "desc": "Depth-First Search"},
                    {"name": "DLS", "desc": "Depth-Limited Search"},
                    {"name": "IDS", "desc": "Iterative Deepening Search"},
                    {"name": "UCS", "desc": "Uniform Cost Search"}
                ]
            },
            {
                "name": "Informed Search",
                "algorithms": [
                    {"name": "Greedy", "desc": "Greedy Best-First Search"},
                    {"name": "A*", "desc": "A* Search"}
                ]
            },
            {
                "name": "Local Search",
                "algorithms": [
                    {"name": "Hill Climbing", "desc": "Hill Climbing Search"},
                    {"name": "Simulated Annealing", "desc": "Simulated Annealing"},
                    {"name": "Beam Search", "desc": "Beam Search"},
                    {"name": "Genetic Algorithm", "desc": "Genetic Algorithm"}
                ]
            },
            {
                "name": "Complex Environment",
                "algorithms": [
                    {"name": "Nondeterministic", "desc": "Nondeterministic Search"},
                    {"name": "Unobservable Search", "desc": "Conformant Planning"},
                    {"name": "Partial Observable", "desc": "Contingency Planning"}
                ]
            },
            {
                "name": "Constraint Satisfied Problem",
                "algorithms": [
                    {"name": "Backtracking", "desc": "Backtracking"},
                    {"name": "Forward Checking", "desc": "Forward Checking"},
                    {"name": "Arc Consistency Algorithm 3", "desc": "Arc Consistency Algorithm 3"}
                ]
            },
            {
                "name": "Machine Learning",
                "algorithms": [
                    {"name": "Q-Learning", "desc": "Q-Learning"},
                    {"name": "Neural Network Path", "desc": "Neural Network Pathfinding"},
                    {"name": "Random Forest Path", "desc": "Random Forest Pathfinding"}
                ]
            }
        ]

    def draw_group_buttons(self):
        start_x = 10
        start_y = BOARD_OFFSET_Y
        for i, group in enumerate(self.algorithm_groups):
            row = i // 2
            col = i % 2
            x = start_x + col * (self.GROUP_BUTTON_WIDTH + self.BUTTON_SPACING)
            y = start_y + row * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            button_rect = pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

            if self.game.selected_group == i:
                # Trạng thái ĐÃ CHỌN: Nền Màu Nhấn (PASTEL_ACCENT)
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE  # Chữ trắng trên nền xanh pastel
            else:
                # Trạng thái KHÔNG CHỌN: Nền Trắng, Viền Màu Nhấn
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, 1, border_radius=self.BUTTON_RADIUS)
                text_color = PASTEL_DARK_TEXT  # Chữ đen-xám đậm

            text = self.small_font.render(group["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_group_button_rect(self, i):
        start_x = 10
        start_y = BOARD_OFFSET_Y
        row = i // 2
        col = i % 2
        x = start_x + col * (self.GROUP_BUTTON_WIDTH + self.BUTTON_SPACING)
        y = start_y + row * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

    def draw_algorithm_buttons(self):
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.algorithm_groups):
            return
            
        start_x = 10
        start_y = BOARD_OFFSET_Y + 3 * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) + 40
        spacing = self.BUTTON_SPACING
        current_group = self.algorithm_groups[self.game.selected_group]
        
        # Tiêu đề nhóm, dùng màu nhấn
        title_text = self.font.render(f"Group: {current_group['name']}", True, PASTEL_ACCENT)
        self.screen.blit(title_text, (start_x, start_y - 30))

        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (self.ALG_BUTTON_HEIGHT + spacing)
            button_rect = pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

            if self.game.selected_algorithm == i:
                # Trạng thái ĐÃ CHỌN: Nền Màu Nhấn (PASTEL_ACCENT)
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, border_radius=self.BUTTON_RADIUS)
                name_color = WHITE
                desc_color = PASTEL_LIGHT_TEXT_ON_ACCENT  # Desc hơi mờ đi để tên thuật toán nổi bật hơn
            else:
                # Trạng thái KHÔNG CHỌN: Nền Trắng, Viền Màu Nhấn
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, PASTEL_LIGHT_BORDER, button_rect, 1, border_radius=self.BUTTON_RADIUS)
                name_color = PASTEL_DARK_TEXT # Tên thuật toán màu đậm
                desc_color = PASTEL_MEDIUM_TEXT # Mô tả màu xám pastel

            name_text = self.small_font.render(algorithm["name"], True, name_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            desc_text = self.small_font.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 30))

    def get_algorithm_button_rect(self, group_index, alg_index):
        start_x = 10
        start_y = BOARD_OFFSET_Y + 3 * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) + 40
        y = start_y + alg_index * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

    def draw_controls(self):
        button_width = 120 # Giữ nguyên hoặc điều chỉnh theo ý bạn
        button_height = 40
        start_x = 20
        start_y = 720
        spacing = 10
        buttons = [
            {"text": "Start", "action": "start"},
            {"text": "Visualize", "action": "visualize"},
            {"text": "Stop", "action": "stop"},
            {"text": "Random Solution", "action": "random_solution"}
        ]
        
        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, start_y, button_width, button_height)
            
            is_active = (
                (button["action"] == "start" or button["action"] == "visualize") or
                (button["action"] == "stop" and self.game.is_running) or
                (button["action"] == "random_solution" and not self.game.is_running)
            )
            
            if is_active:
                # Nút active: nền Màu Nhấn
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE
            else:
                # Nút KHÔNG ACTIVE (Thụ động): Nền Xám Thụ động, Viền Xám, Chữ Xám
                pygame.draw.rect(self.screen, DISABLED_BG, button_rect, border_radius=self.BUTTON_RADIUS) 
                pygame.draw.rect(self.screen, DISABLED_TEXT, button_rect, 1, border_radius=self.BUTTON_RADIUS)
                text_color = DISABLED_TEXT # <-- Dùng màu chữ thụ động
            
            text = self.small_font.render(button["text"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_control_button_rect(self, i):
        button_width = 110
        button_height = 38
        start_x = 20
        start_y = 720
        spacing = 10
        x = start_x + i * (button_width + spacing)
        return pygame.Rect(x, start_y, button_width, button_height)

    def draw_stats_and_history(self):
        stats_x = 1400 - 300 - 20
        stats_y = BOARD_OFFSET_Y 
        stats_rect = pygame.Rect(stats_x, stats_y, 300, STATS_HEIGHT)
        
        # Nền trắng, viền pastel nhẹ hơn một chút
        shadow_rect = pygame.Rect(stats_x + 3, stats_y + 3, 300, STATS_HEIGHT)
        pygame.draw.rect(self.screen, (190, 210, 220), shadow_rect, border_radius=self.BUTTON_RADIUS)
        
        # Nền trắng, viền rõ ràng hơn
        pygame.draw.rect(self.screen, WHITE, stats_rect, border_radius=self.BUTTON_RADIUS)
        pygame.draw.rect(self.screen, PASTEL_LIGHT_BORDER, stats_rect, 1, border_radius=self.BUTTON_RADIUS)

        # Sử dụng PASTEL_DARK_TEXT mới
        title = self.font.render("Current Run", True, PASTEL_DARK_TEXT)
        self.screen.blit(title, (stats_x + 10, stats_y + 10))
        
        stats_info = [
            f"Nodes Visited: {self.game.stats['nodes_visited']}",
            f"Path Length: {self.game.stats['path_length']}",
            f"Time: {self.game.stats['time']:.0f}ms",
            f"Status: {'Running' if self.game.is_running else 'Stopped'}"
        ]

        for i, info in enumerate(stats_info):
            # Sử dụng PASTEL_ACCENT cho Nodes và Path, PASTEL_DARK_TEXT cho các thông tin khác
            text_color = PASTEL_ACCENT if (i == 0 or i == 1) else PASTEL_DARK_TEXT
            text = self.small_font.render(info, True, text_color)
            self.screen.blit(text, (stats_x + 10, stats_y + 40 + i * 20))

        # Sử dụng PASTEL_LIGHT_BORDER mới
        pygame.draw.line(self.screen, PASTEL_LIGHT_BORDER, (stats_x + 10, stats_y + 130), (stats_x + 290, stats_y + 130), 1)
        # Sử dụng PASTEL_DARK_TEXT mới
        history_title = self.font.render("History", True, PASTEL_DARK_TEXT)
        self.screen.blit(history_title, (stats_x + 10, stats_y + 140))
        
        if not self.game.history:
            # Sử dụng PASTEL_MEDIUM_TEXT mới
            no_data = self.small_font.render("No data available", True, PASTEL_MEDIUM_TEXT)
            self.screen.blit(no_data, (stats_x + 10, stats_y + 170))
        else:
            recent_runs = self.game.history[:5]
            for i, record in enumerate(recent_runs):
                base_y = stats_y + 170 + i * 40
                # Sử dụng PASTEL_DARK_TEXT mới
                name_text = self.small_font.render(f"{record['name']}", True, PASTEL_DARK_TEXT)
                self.screen.blit(name_text, (stats_x + 10, base_y))

                info_text = self.small_font.render(
                f"Nodes:{record['nodes']}  Len:{record['length']}  Time:{record['time']}",
                True, PASTEL_MEDIUM_TEXT # <-- Dùng màu chữ phụ mới
                )
                self.screen.blit(info_text, (stats_x + 10, base_y + 18))

    def draw_board(self, x_start, y_start, rooks=None, cell_size=SMALL_CELL_SIZE):
        board_size = 8 * cell_size
        board_rect = pygame.Rect(x_start, y_start, board_size, board_size)
        for r in range(8):
            for c in range(8):
                x1, y1 = x_start + c * cell_size, y_start + r * cell_size
                # Dùng màu bàn cờ pastel mới
                color = BOARD_LIGHT_CELL if (r + c) % 2 == 0 else BOARD_DARK_CELL
                pygame.draw.rect(self.screen, color, (x1, y1, cell_size, cell_size))
                
        pygame.draw.rect(self.screen, PASTEL_LIGHT_BORDER, board_rect, 1) # Vẽ viền 1px

        # Chữ tọa độ bàn cờ dùng màu đậm để dễ nhìn
        for c in range(8):
            x_center = x_start + c * cell_size + cell_size // 2
            text = self.small_font.render(chr(ord('a') + c), True, PASTEL_MEDIUM_TEXT) 
            text_rect = text.get_rect(center=(x_center, y_start + 8 * cell_size + 10))
            self.screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(x_center, y_start - 10))
            self.screen.blit(text, text_rect)

        for r in range(8):
            y_center = y_start + r * cell_size + cell_size // 2
            text = self.small_font.render(str(8 - r), True, PASTEL_MEDIUM_TEXT) 
            text_rect = text.get_rect(center=(x_start - 10, y_center))
            self.screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(x_start + 8 * cell_size + 10, y_center))
            self.screen.blit(text, text_rect)

        if rooks and self.rook_img:
            for r, c in rooks:
                x_center = x_start + c * cell_size + cell_size // 2
                y_center = y_start + r * cell_size + cell_size // 2
                rook_rect = self.rook_img.get_rect(center=(x_center, y_center))
                self.screen.blit(self.rook_img, rook_rect)

    def draw_start_goal(self):
        self.draw_board(BOARD_OFFSET_X, BOARD_OFFSET_Y, cell_size=SMALL_CELL_SIZE)
        start_text = self.font.render("Start", True, PASTEL_DARK_TEXT) # Đổi màu chữ
        self.screen.blit(start_text, (BOARD_OFFSET_X + 4 * SMALL_CELL_SIZE - start_text.get_width() // 2, 
                                       BOARD_OFFSET_Y + 8 * SMALL_CELL_SIZE + 20))
        
        goal_rooks = [(r, self.game.solution[r]) for r in range(8)]
        self.draw_board(BOARD_OFFSET_X + 8 * SMALL_CELL_SIZE + 40, BOARD_OFFSET_Y, goal_rooks, cell_size=SMALL_CELL_SIZE)
        goal_text = self.font.render("Goal", True, PASTEL_DARK_TEXT) # Đổi màu chữ
        self.screen.blit(goal_text, (BOARD_OFFSET_X + 8 * SMALL_CELL_SIZE + 40 + 4 * SMALL_CELL_SIZE - goal_text.get_width() // 2, 
                                      BOARD_OFFSET_Y + 8 * SMALL_CELL_SIZE + 20))
    def draw_all(self):
        
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats_and_history()
        self.draw_start_goal()
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (64, 64, 64)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 140, 0)
CYAN = (0, 200, 200)
PINK = (255, 192, 203)
LIGHT_BLUE = (173, 216, 230)

# Board constants
BOARD_OFFSET_X = 400
BOARD_OFFSET_Y = 80
RIGHT_SIDE_PANEL_WIDTH = 180
LEGEND_HEIGHT = 210
STATS_HEIGHT = 380
SMALL_CELL_SIZE = 37

GRADIENTS = {
    "purple_blue": ((147, 51, 234), (59, 130, 246)),
    "cyan_blue": ((6, 182, 212), (59, 130, 246)),
    "green_blue": ((74, 222, 128), (37, 99, 235)),
    "purple_pink": ((168, 85, 247), (236, 72, 153)),
    "pink_orange": ((236, 72, 153), (251, 146, 60)),
    "teal_lime": ((153, 246, 228), (217, 249, 157)),
    "red_yellow": ((254, 202, 202), (252, 165, 165), (254, 240, 138))
}

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
                "gradient": "cyan_blue",
                "text_color": WHITE,
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
                "gradient": "green_blue",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Greedy", "desc": "Greedy Best-First Search"},
                    {"name": "A*", "desc": "A* Search"}
                ]
            },
            {
                "name": "Local Search",
                "gradient": "purple_pink",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Hill Climbing", "desc": "Hill Climbing Search"},
                    {"name": "Simulated Annealing", "desc": "Simulated Annealing"},
                    {"name": "Beam Search", "desc": "Beam Search"},
                    {"name": "Genetic Algorithm", "desc": "Genetic Algorithm"}
                ]
            },
            {
                "name": "Complex Environment",
                "gradient": "pink_orange",
                "text_color": WHITE,
                "algorithms": [
                    {"name": "Nondeterministic", "desc": "Nondeterministic Search"},
                    {"name": "Unobservable Search", "desc": "Conformant Planning"},
                    {"name": "Partial Observable", "desc": "Contingency Planning"}
                ]
            },
            {
                "name": "Constraint Satisfied Problem",
                "gradient": "teal_lime",
                "text_color": BLACK,
                "algorithms": [
                    {"name": "Backtracking", "desc": "Backtracking"},
                    {"name": "Forward Checking", "desc": "Forward Checking"},
                    {"name": "Arc Consistency Algorithm 3", "desc": "Arc Consistency Algorithm 3"}
                ]
            },
            {
                "name": "Machine Learning",
                "gradient": "red_yellow",
                "text_color": BLACK,
                "algorithms": [
                    {"name": "Q-Learning", "desc": "Q-Learning"},
                    {"name": "Neural Network Path", "desc": "Neural Network Pathfinding"},
                    {"name": "Random Forest Path", "desc": "Random Forest Pathfinding"}
                ]
            }
        ]

    @staticmethod
    def draw_gradient_rect(surface, rect, color1, color2, color3=None, vertical=True, border_radius=0):
        x, y, w, h = rect
        temp_surface = pygame.Surface((w, h), pygame.SRCALPHA)

        if color3 is None:
            steps = h if vertical else w
            for i in range(steps):
                ratio = i / steps
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                if vertical:
                    pygame.draw.line(temp_surface, (r, g, b), (0, i), (w, i))
                else:
                    pygame.draw.line(temp_surface, (r, g, b), (i, 0), (i, h))
        else:
            steps = h if vertical else w
            mid = steps // 2
            for i in range(steps):
                if i < mid:
                    ratio = i / mid
                    r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                    g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                    b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                else:
                    ratio = (i - mid) / (steps - mid)
                    r = int(color2[0] * (1 - ratio) + color3[0] * ratio)
                    g = int(color2[1] * (1 - ratio) + color3[1] * ratio)
                    b = int(color2[2] * (1 - ratio) + color3[2] * ratio)
                if vertical:
                    pygame.draw.line(temp_surface, (r, g, b), (0, i), (w, i))
                else:
                    pygame.draw.line(temp_surface, (r, g, b), (i, 0), (i, h))

        mask = pygame.Surface((w, h), pygame.SRCALPHA)
        pygame.draw.rect(mask, (255, 255, 255, 255), (0, 0, w, h), border_radius=border_radius)
        temp_surface.blit(mask, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
        surface.blit(temp_surface, (x, y))

    def draw_group_buttons(self):
        start_x = 10
        start_y = BOARD_OFFSET_Y
        for i, group in enumerate(self.algorithm_groups):
            row = i // 2
            col = i % 2
            x = start_x + col * (self.GROUP_BUTTON_WIDTH + self.BUTTON_SPACING)
            y = start_y + row * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            button_rect = pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)
            gradient_key = group.get("gradient", "purple_blue")
            colors = GRADIENTS[gradient_key]

            if self.game.selected_group == i:
                if len(colors) == 2:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], vertical=False, border_radius=self.BUTTON_RADIUS)
                else:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], colors[2], vertical=False, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = group.get("text_color", WHITE)
            else:
                c1, c2 = GRADIENTS["purple_blue"]
                self.draw_gradient_rect(self.screen, button_rect, c1, c2, vertical=False, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE

            text = self.font.render(group["name"], True, text_color)
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
        gradient_key = current_group.get("gradient", "purple_blue")
        colors = GRADIENTS[gradient_key]
        main_color = colors[0]

        title_text = self.font.render(f"Group: {current_group['name']}", True, (147, 51, 234))
        self.screen.blit(title_text, (start_x, start_y - 30))

        for i, algorithm in enumerate(current_group["algorithms"]):
            y = start_y + i * (self.ALG_BUTTON_HEIGHT + spacing)
            button_rect = pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

            if self.game.selected_algorithm == i:
                if len(colors) == 2:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], vertical=False, border_radius=self.BUTTON_RADIUS)
                else:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], colors[2], vertical=False, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = current_group.get("text_color", WHITE)
                desc_color = current_group.get("text_color", WHITE)
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, main_color, button_rect, 1, border_radius=self.BUTTON_RADIUS)
                c1, c2 = GRADIENTS["purple_blue"]
                text_color = c1
                desc_color = c2

            name_text = self.small_font.render(algorithm["name"], True, text_color)
            self.screen.blit(name_text, (start_x + 10, y + 8))
            desc_text = self.small_font.render(algorithm["desc"], True, desc_color)
            self.screen.blit(desc_text, (start_x + 10, y + 30))

    def get_algorithm_button_rect(self, group_index, alg_index):
        start_x = 10
        start_y = BOARD_OFFSET_Y + 3 * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) + 40
        y = start_y + alg_index * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)

    def draw_controls(self):
        button_width = 120
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
        current_group = self.algorithm_groups[self.game.selected_group]
        gradient_key = current_group.get("gradient", "purple_blue")
        colors = GRADIENTS[gradient_key]

        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, start_y, button_width, button_height)
            # Kiểm tra trạng thái active của nút
            is_active = (
                (button["action"] == "start" or button["action"] == "visualize") or
                (button["action"] == "stop" and self.game.is_running) or
                (button["action"] == "random_solution" and not self.game.is_running)
            )
            
            if is_active:
                # Nút active: dùng gradient của nhóm thuật toán hiện tại
                if len(colors) == 2:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], vertical=False, border_radius=self.BUTTON_RADIUS)
                else:
                    self.draw_gradient_rect(self.screen, button_rect, colors[0], colors[1], colors[2], vertical=False, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = BLACK  # Chữ đen khi active
            else:
                # Nút không active: nền xám
                pygame.draw.rect(self.screen, (180, 180, 180), button_rect, border_radius=self.BUTTON_RADIUS)  # xám nhạt
                pygame.draw.rect(self.screen, BLACK, button_rect, 2, border_radius=self.BUTTON_RADIUS)
                text_color = BLACK  # chữ vẫn để đen hoặc bạn có thể chỉnh thành trắng cho dễ nhìn

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
        pygame.draw.rect(self.screen, LIGHT_GRAY, stats_rect)
        pygame.draw.rect(self.screen, BLACK, stats_rect, 2)

        title = self.font.render("Current Run", True, BLACK)
        self.screen.blit(title, (stats_x + 10, stats_y + 10))
        stats_info = [
            f"Nodes Visited: {self.game.stats['nodes_visited']}",
            f"Path Length: {self.game.stats['path_length']}",
            f"Time: {self.game.stats['time']:.0f}ms",
            f"Status: {'Running' if self.game.is_running else 'Stopped'}"
        ]

        for i, info in enumerate(stats_info):
            text = self.small_font.render(info, True, BLACK)
            self.screen.blit(text, (stats_x + 10, stats_y + 40 + i * 20))

        pygame.draw.line(self.screen, DARK_GRAY, (stats_x + 10, stats_y + 130), (stats_x + 290, stats_y + 130), 2)
        history_title = self.font.render("History", True, BLACK)
        self.screen.blit(history_title, (stats_x + 10, stats_y + 140))

        if not self.game.history:
            no_data = self.small_font.render("No data available", True, GRAY)
            self.screen.blit(no_data, (stats_x + 10, stats_y + 170))
        else:
            # Hiển thị tối đa 5 bản ghi gần nhất
            recent_runs = self.game.history[:5]

            for i, record in enumerate(recent_runs):
                base_y = stats_y + 170 + i * 40  # cách dòng 40px
                name_text = self.small_font.render(f"{record['name']}", True, BLACK)
                self.screen.blit(name_text, (stats_x + 10, base_y))

                info_text = self.small_font.render(
                    f"Nodes:{record['nodes']}  Len:{record['length']}  Time:{record['time']}",
                    True, DARK_GRAY
                )
                self.screen.blit(info_text, (stats_x + 10, base_y + 18))

    def draw_board(self, x_start, y_start, rooks=None, cell_size=SMALL_CELL_SIZE):
        for r in range(8):
            for c in range(8):
                x1, y1 = x_start + c * cell_size, y_start + r * cell_size
                color = (240, 217, 181) if (r + c) % 2 == 0 else (181, 136, 99)
                pygame.draw.rect(self.screen, color, (x1, y1, cell_size, cell_size))

        for c in range(8):
            x_center = x_start + c * cell_size + cell_size // 2
            text = self.small_font.render(chr(ord('a') + c), True, BLACK)
            text_rect = text.get_rect(center=(x_center, y_start + 8 * cell_size + 10))
            self.screen.blit(text, text_rect)
            text_rect = text.get_rect(center=(x_center, y_start - 10))
            self.screen.blit(text, text_rect)

        for r in range(8):
            y_center = y_start + r * cell_size + cell_size // 2
            text = self.small_font.render(str(8 - r), True, BLACK)
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
        start_text = self.font.render("Start", True, BLACK)
        self.screen.blit(start_text, (BOARD_OFFSET_X + 4 * SMALL_CELL_SIZE - start_text.get_width() // 2, 
                                      BOARD_OFFSET_Y + 8 * SMALL_CELL_SIZE + 20))
        
        goal_rooks = [(r, self.game.solution[r]) for r in range(8)]
        self.draw_board(BOARD_OFFSET_X + 8 * SMALL_CELL_SIZE + 40, BOARD_OFFSET_Y, goal_rooks, cell_size=SMALL_CELL_SIZE)
        goal_text = self.font.render("Goal", True, BLACK)
        self.screen.blit(goal_text, (BOARD_OFFSET_X + 8 * SMALL_CELL_SIZE + 40 + 4 * SMALL_CELL_SIZE - goal_text.get_width() // 2, 
                                     BOARD_OFFSET_Y + 8 * SMALL_CELL_SIZE + 20))

    def draw_all(self):
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats_and_history()
        self.draw_start_goal()
import pygame

# Board constants
BOARD_OFFSET_X = 400
BOARD_OFFSET_Y = 30
STATS_HEIGHT = 380
SMALL_CELL_SIZE = 37
# Hằng số mới cho State Log
LOG_BOARD_HEIGHT = 8 * SMALL_CELL_SIZE + 20 
LOG_PANEL_HEIGHT = 300 
LOG_PANEL_WIDTH = (8 * SMALL_CELL_SIZE * 2) + 40 + 40
LOG_PANEL_Y = BOARD_OFFSET_Y + LOG_BOARD_HEIGHT + 30 
LOG_START_X = BOARD_OFFSET_X - 15 
LOG_LINE_HEIGHT = 18 

# Colors 
WHITE = (255, 255, 255) 

PASTEL_BG = (230, 240, 245)           # Nền chính 
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

        self.GROUP_BUTTON_WIDTH = 250
        self.GROUP_BUTTON_HEIGHT = 55
        self.ALG_BUTTON_WIDTH = 250
        self.ALG_BUTTON_HEIGHT = 55
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
            }
        ]

    def draw_group_buttons(self):
        start_x = 40 
        start_y = BOARD_OFFSET_Y
        for i, group in enumerate(self.algorithm_groups):
            x = start_x
            y = start_y + i * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
            button_rect = pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

            if self.game.selected_group == i:
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, border_radius=self.BUTTON_RADIUS)
                text_color = WHITE
            else:
                pygame.draw.rect(self.screen, WHITE, button_rect, border_radius=self.BUTTON_RADIUS)
                pygame.draw.rect(self.screen, PASTEL_ACCENT, button_rect, 1, border_radius=self.BUTTON_RADIUS)
                text_color = PASTEL_DARK_TEXT

            text = self.small_font.render(group["name"], True, text_color)
            text_rect = text.get_rect(center=button_rect.center)
            self.screen.blit(text, text_rect)

    def get_group_button_rect(self, i):
        start_x = 40
        start_y = BOARD_OFFSET_Y
        x = start_x
        y = start_y + i * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(x, y, self.GROUP_BUTTON_WIDTH, self.GROUP_BUTTON_HEIGHT)

    def draw_algorithm_buttons(self):
        if self.game.selected_group < 0 or self.game.selected_group >= len(self.algorithm_groups):
            return
            
        start_x = 40
        start_y = BOARD_OFFSET_Y + len(self.algorithm_groups) * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) + 50
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
        start_x = 40
        start_y = BOARD_OFFSET_Y + len(self.algorithm_groups) * (self.GROUP_BUTTON_HEIGHT + self.BUTTON_SPACING) + 50
        y = start_y + alg_index * (self.ALG_BUTTON_HEIGHT + self.BUTTON_SPACING)
        return pygame.Rect(start_x, y, self.ALG_BUTTON_WIDTH, self.ALG_BUTTON_HEIGHT)
    
    def draw_controls(self):
        button_width = 120 # Giữ nguyên hoặc điều chỉnh theo ý bạn
        button_height = 40
        start_x = 405
        start_y = 720
        spacing = 10
        buttons = [
            {"text": "Start", "action": "start"},
            {"text": "Visualize", "action": "visualize"},
            {"text": "Stop", "action": "stop"},
            {"text": "Random Solution", "action": "random_solution"},
            {"text": "Statistics", "action": "statistics"},
        ]
        
        for i, button in enumerate(buttons):
            x = start_x + i * (button_width + spacing)
            button_rect = pygame.Rect(x, start_y, button_width, button_height)
            
            is_active = False 
            action = button["action"]

            if action in ["start", "visualize"] and not self.game.is_running:
                is_active = True
            elif action == "stop" and self.game.is_running:
                is_active = True
            elif action == "random_solution" and not self.game.is_running:
                is_active = True
            elif action == "statistics" and self.game.history: 
                is_active = True
            
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
        button_width = 120
        button_height = 40
        start_x = 405
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
        
    def draw_state_log(self):
        
        log_rect = pygame.Rect(LOG_START_X, LOG_PANEL_Y, LOG_PANEL_WIDTH, LOG_PANEL_HEIGHT)  
        # Nền, viền khung panel
        pygame.draw.rect(self.screen, WHITE, log_rect, border_radius=self.BUTTON_RADIUS)
        pygame.draw.rect(self.screen, PASTEL_LIGHT_BORDER, log_rect, 1, border_radius=self.BUTTON_RADIUS)

        # Tiêu đề
        title = self.font.render("State Log (Real-time Search)", True, PASTEL_DARK_TEXT)
        self.screen.blit(title, (log_rect.x + 10, log_rect.y + 5))
        
        # Thiết lập Viewport
        viewport_rect = log_rect.copy()
        viewport_rect.y += 30 # Bắt đầu sau tiêu đề
        viewport_rect.height -= 30 
        
        if not self.game.state_log:
            return

        total_log_height = len(self.game.state_log) * LOG_LINE_HEIGHT
        content_surface_height = max(viewport_rect.height, total_log_height)
        
        content_surface_height += 5

        content_surface = pygame.Surface((viewport_rect.width - 20, content_surface_height))
        content_surface.fill(WHITE) 

        for i, entry in enumerate(self.game.state_log):
            y_pos = i * LOG_LINE_HEIGHT
            text = self.small_font.render(entry, True, PASTEL_MEDIUM_TEXT)
            content_surface.blit(text, (0, y_pos))

        viewport_offset_x = viewport_rect.x + 10
        viewport_offset_y = viewport_rect.y
        
        source_rect = pygame.Rect(0, self.game.log_scroll_offset, viewport_rect.width - 20, viewport_rect.height)

        self.screen.blit(content_surface, 
                         (viewport_offset_x, viewport_offset_y), 
                         source_rect)
        
    def draw_stats_panel(self):
        """**CẬP NHẬT:** Vẽ bảng thống kê với giao diện tab."""
        # Lớp phủ mờ
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((PASTEL_BG[0], PASTEL_BG[1], PASTEL_BG[2], 220))
        self.screen.blit(overlay, (0, 0))

        panel_width = 900
        panel_height = 600
        panel_x = (self.screen.get_width() - panel_width) // 2
        panel_y = (self.screen.get_height() - panel_height) // 2
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)

        # Vẽ khung panel
        pygame.draw.rect(self.screen, WHITE, panel_rect, border_radius=self.BUTTON_RADIUS)
        pygame.draw.rect(self.screen, PASTEL_LIGHT_BORDER, panel_rect, 2, border_radius=self.BUTTON_RADIUS)

        # Tiêu đề & Nút đóng
        title_text = self.game.title_font.render("Performance Statistics", True, PASTEL_DARK_TEXT)
        self.screen.blit(title_text, (panel_x + 20, panel_y + 15))
        close_rect = self.get_stats_panel_close_button_rect()
        pygame.draw.rect(self.screen, (255, 100, 100), close_rect, border_radius=5)
        close_text = self.font.render("X", True, WHITE)
        self.screen.blit(close_text, close_text.get_rect(center=close_rect.center))

        # ---- Vẽ các Tab ----
        tab_names = {1: "Overall Stats", 2: "Success Analysis", 3: "Group Champions"}
        for i in range(1, 4):
            tab_rect = self.get_stats_tab_rect(i)
            if self.game.stats_active_tab == i:
                pygame.draw.rect(self.screen, PASTEL_ACCENT, tab_rect, border_top_left_radius=8, border_top_right_radius=8)
                text_color = WHITE
            else:
                pygame.draw.rect(self.screen, DISABLED_BG, tab_rect, border_top_left_radius=8, border_top_right_radius=8)
                text_color = PASTEL_MEDIUM_TEXT
            tab_text = self.small_font.render(tab_names[i], True, text_color)
            self.screen.blit(tab_text, tab_text.get_rect(center=tab_rect.center))
        
        # ---- Vẽ nội dung của Tab ----
        content_y_start = panel_y + 100
        active_tab = self.game.stats_active_tab
        
        if active_tab == 1:
            stats_source = self.game.calculated_stats.get("all_runs")
            if not stats_source:
                self.draw_no_data_message(panel_x, content_y_start)
                return
            self.draw_stats_table(panel_x, content_y_start, panel_width, list(stats_source.items()))
        
        elif active_tab == 2:
            stats_source = self.game.calculated_stats.get("successful_runs")
            if not stats_source:
                self.draw_no_data_message(panel_x, content_y_start, "No successful runs (length=8) recorded yet.")
                return
            # Dữ liệu cho biểu đồ Tab 2 là danh sách các thuật toán thành công
            chart_data = list(stats_source.items())
            # Đổi tên nhãn để rõ ràng hơn
            chart_data_renamed = [(alg_data['name'], alg_data) for _, alg_data in chart_data]
            self.draw_stats_charts(panel_x, content_y_start, panel_width, chart_data_renamed)

        elif active_tab == 3:
            stats_source = self.game.calculated_stats.get("group_bests")
            if not stats_source:
                self.draw_no_data_message(panel_x, content_y_start, "No successful runs to analyze by group.")
                return
            # Dữ liệu cho biểu đồ Tab 3 là danh sách các nhóm và "nhà vô địch" của chúng
            chart_data = list(stats_source.items())
            self.draw_group_charts(panel_x, content_y_start, panel_width, chart_data)
    def draw_bar_chart(self, x, y, width, height, data, data_key, title, color, show_champion_name=False):
        """
        Vẽ một biểu đồ thanh ngang (Horizontal Bar Chart) hoàn chỉnh.
        - Sắp xếp các thanh từ dài nhất đến ngắn nhất.
        - Hiển thị tên (thuật toán hoặc nhóm) ở bên trái.
        - Hiển thị giá trị ở cuối mỗi thanh.
        - Có thể tùy chọn hiển thị tên "nhà vô địch" cho biểu đồ nhóm.
        """
        # 1. Vẽ tiêu đề biểu đồ
        chart_title_text = self.font.render(title, True, PASTEL_DARK_TEXT)
        self.screen.blit(chart_title_text, chart_title_text.get_rect(centerx=x + width / 2, y=y))

        # 2. Xác định khu vực vẽ chính
        # Trục Y (dọc) là nơi chứa tên
        label_area_width = 150  # Dành không gian bên trái cho tên
        plot_area_x = x + label_area_width
        plot_width = width - label_area_width - 10

        # Trục X (ngang) là thang đo giá trị
        plot_area_y = y + 40
        plot_height = height - 60
        plot_right_x = plot_area_x + plot_width

        # 3. Vẽ các trục tọa độ
        pygame.draw.line(self.screen, PASTEL_LIGHT_BORDER, (plot_area_x, plot_area_y), (plot_area_x, plot_area_y + plot_height), 2)
        pygame.draw.line(self.screen, PASTEL_LIGHT_BORDER, (plot_area_x, plot_area_y + plot_height), (plot_right_x, plot_area_y + plot_height), 2)

        if not data:
            return

        # 4. Sắp xếp dữ liệu để thanh dài nhất luôn ở trên cùng
        data.sort(key=lambda item: item[1][data_key], reverse=True)

        # 5. Xác định thang đo và vẽ các mốc giá trị
        max_value = data[0][1][data_key] if data else 0
        if max_value == 0: max_value = 1

        max_label = self.small_font.render(f"{max_value:.0f}", True, PASTEL_MEDIUM_TEXT)
        mid_label = self.small_font.render(f"{max_value/2:.0f}", True, PASTEL_MEDIUM_TEXT)
        self.screen.blit(max_label, max_label.get_rect(midtop=(plot_right_x, plot_area_y + plot_height + 5)))
        self.screen.blit(mid_label, mid_label.get_rect(midtop=(plot_area_x + plot_width / 2, plot_area_y + plot_height + 5)))

        # 6. Tính toán kích thước và vẽ từng thanh
        num_items = len(data)
        total_bar_height_area = plot_height - 20
        bar_spacing = 5
        bar_height = max(2, (total_bar_height_area - (num_items - 1) * bar_spacing) / num_items if num_items > 0 else 0)

        for i, (label_name, stats_data) in enumerate(data):
            value = stats_data[data_key]
            
            # Tính chiều dài và vị trí
            bar_length = (value / max_value) * plot_width
            bar_x = plot_area_x
            bar_y = plot_area_y + 10 + i * (bar_height + bar_spacing)
            
            # Vẽ thanh
            bar_rect = pygame.Rect(bar_x, bar_y, bar_length, bar_height)
            pygame.draw.rect(self.screen, color, bar_rect, border_top_right_radius=4, border_bottom_right_radius=4)

            # 7. Vẽ nhãn tên (tùy chỉnh cho 2 loại biểu đồ)
            main_label_text = self.small_font.render(label_name, True, PASTEL_DARK_TEXT)
            
            if show_champion_name:
                # Dành cho Tab 3: Hiển thị tên Nhóm và tên "nhà vô địch"
                self.screen.blit(main_label_text, main_label_text.get_rect(midright=(bar_x - 10, bar_y + bar_height / 2 - 5)))
                champion_name = stats_data.get('name', '')
                champion_text = pygame.font.SysFont("segoeui", 11).render(f"({champion_name})", True, PASTEL_MEDIUM_TEXT)
                self.screen.blit(champion_text, champion_text.get_rect(midright=(bar_x - 10, bar_y + bar_height / 2 + 10)))
            else:
                # Dành cho Tab 2: Chỉ hiển thị tên thuật toán
                self.screen.blit(main_label_text, main_label_text.get_rect(midright=(bar_x - 10, bar_y + bar_height / 2)))

            # 8. Vẽ nhãn giá trị ở cuối thanh
            value_text_surface = self.small_font.render(f"{value:.0f}", True, color)
            if bar_length > 50: # Nếu thanh đủ dài, đặt giá trị bên trong
                self.screen.blit(value_text_surface, value_text_surface.get_rect(midright=(bar_x + bar_length - 5, bar_y + bar_height / 2)))
            else: # Nếu thanh ngắn, đặt giá trị bên ngoài
                self.screen.blit(value_text_surface, value_text_surface.get_rect(midleft=(bar_x + bar_length + 5, bar_y + bar_height / 2)))
    
    def get_stats_panel_close_button_rect(self):
        panel_width = 900
        panel_x = (self.screen.get_width() - panel_width) // 2
        panel_y = (self.screen.get_height() - 600) // 2
        return pygame.Rect(panel_x + panel_width - 40, panel_y + 15, 25, 25)
    
    def get_stats_tab_rect(self, tab_index):
        panel_x = (self.screen.get_width() - 900) // 2
        panel_y = (self.screen.get_height() - 600) // 2
        tab_width = 200
        tab_height = 30
        return pygame.Rect(panel_x + 10 + (tab_index - 1) * (tab_width + 5), panel_y + 60, tab_width, tab_height)
    
    def draw_no_data_message(self, panel_x, y_start, message="No data available to display."):
        """Vẽ thông báo khi không có dữ liệu."""
        no_data_text = self.font.render(message, True, PASTEL_MEDIUM_TEXT)
        self.screen.blit(no_data_text, (panel_x + 40, y_start + 40))
    
    def draw_stats_table(self, panel_x, y_start, panel_width, data):
        """Vẽ bảng dữ liệu cho Tab 1."""
        header_y = y_start + 10
        headers = ["Algorithm", "Runs", "Avg Nodes", "Avg Time (ms)", "Avg Length", "Success %"]
        col_starts = [panel_x + 30, panel_x + 280, panel_x + 380, panel_x + 530, panel_x + 680, panel_x + 810]
        for i, header in enumerate(headers):
            header_text = self.small_font.render(header, True, PASTEL_ACCENT)
            self.screen.blit(header_text, (col_starts[i], header_y))
            
        pygame.draw.line(self.screen, PASTEL_LIGHT_BORDER, (panel_x + 20, header_y + 25), (panel_x + panel_width - 20, header_y + 25))

        current_y = header_y + 35
        for alg_name, alg_data in data:
            row_data = [
                alg_name, f"{alg_data['runs']}", f"{alg_data['avg_nodes']:.0f}",
                f"{alg_data['avg_time']:.0f}", f"{alg_data['avg_length']:.1f}", f"{alg_data['success_rate']:.0%}"
            ]
            for i, item in enumerate(row_data):
                item_text = self.small_font.render(item, True, PASTEL_DARK_TEXT)
                self.screen.blit(item_text, (col_starts[i], current_y))
            current_y += 25
            if current_y > y_start + 450: break
            
    def draw_stats_charts(self, panel_x, y_start, panel_width, data):
        """Vẽ biểu đồ cho Tab 2."""
        chart_area_y = y_start + 20
        chart_height = 400

        chart1_x = panel_x + 50
        chart1_width = 380
        self.draw_bar_chart(
            x=chart1_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_nodes', title='Average Nodes (Success Cases)',
            color=(100, 130, 180)
        )

        chart2_x = panel_x + panel_width - chart1_width - 50
        self.draw_bar_chart(
            x=chart2_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_time', title='Average Time (ms) (Success Cases)',
            color=(110, 180, 130)
        )    
    
    def draw_stats_charts(self, panel_x, y_start, panel_width, data):
        """Vẽ biểu đồ so sánh giữa các thuật toán riêng lẻ (Tab 2)."""
        chart_area_y = y_start + 20
        chart_height = 400

        chart1_x = panel_x + 50
        chart1_width = 380
        self.draw_bar_chart(
            x=chart1_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_nodes', title='Average Nodes (Success Cases)',
            color=(100, 130, 180)
        )

        chart2_x = panel_x + panel_width - chart1_width - 50
        self.draw_bar_chart(
            x=chart2_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_time', title='Average Time (ms) (Success Cases)',
            color=(110, 180, 130)
        )

    def draw_group_charts(self, panel_x, y_start, panel_width, data):
        """Vẽ biểu đồ so sánh giữa các nhóm thuật toán (Tab 3)."""
        chart_area_y = y_start + 20
        chart_height = 400

        chart1_x = panel_x + 50
        chart1_width = 380
        self.draw_bar_chart(
            x=chart1_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_nodes', title='Average Nodes (Group Champions)',
            color=(100, 130, 180),
            show_champion_name=True
        )

        chart2_x = panel_x + panel_width - chart1_width - 50
        self.draw_bar_chart(
            x=chart2_x, y=chart_area_y, width=chart1_width, height=chart_height,
            data=data, data_key='avg_time', title='Average Time (ms) (Group Champions)',
            color=(110, 180, 130),
            show_champion_name=True
        ) 
            
    def draw_all(self):
        
        self.draw_group_buttons()
        self.draw_algorithm_buttons()
        self.draw_controls()
        self.draw_stats_and_history()
        self.draw_start_goal()
        self.draw_state_log()
        
    
# BÁO CÁO BÀI TOÁN 8 QUÂN XE

**GVHD**: Phan Thị Huyền Trang  
**SVTT**: Nguyễn Trường Minh - **MSSV**: 23110125

# BÀI TOÁN 8 QUÂN XE

## 1. Giới thiệu bài toán

### Mô tả
Bài toán 8 quân xe là một trong những bài toán kinh điển của trí tuệ nhân tạo và lý thuyết thuật toán.
**Mục tiêu**: Đặt 8 quân Xe (Rook) lên bàn cờ vua 8×8 sao cho không có quân nào ăn được lẫn nhau.

Một quân Xe có thể tấn công theo:
- Hàng ngang
- Cột dọc

### Mô hình PEAS

- **P (Performance measure - Đo lường hiệu suất):** Đặt đủ 8 quân Xe mà không có quân nào ăn nhau.
- **E (Environment - Môi trường):** Bàn cờ vua 8×8.
- **A (Actuators - Bộ truyền động):** Đặt một quân Xe vào một ô trống trên bàn cờ.
- **S (Sensors - Cảm biến):** Trạng thái bàn cờ (vị trí các quân xe đã đặt, các ràng buộc).

## 2. Các thuật toán được áp dụng

⚠️ **Lưu ý**: Để tối ưu hóa và quản lý bộ nhớ, việc sinh trạng thái trong hầu hết các thuật toán đều được thực hiện theo từng hàng.

---

### 2.1. Nhóm thuật toán tìm kiếm không có thông tin (Uninformed Search)

#### 1. Tìm kiếm theo chiều rộng (BFS)

* **Mô tả**: Tìm kiếm theo chiều rộng ([Breadth-First Search](https://vi.wikipedia.org/wiki/T%C3%ACm_ki%E1%BA%BFm_theo_chi%E1%BB%81u_r%E1%BB%99ng)) duyệt qua các node theo từng mức, đảm bảo tìm thấy đường đi ngắn nhất về số bước.
* **Các bước thực hiện trong code**:
    1.  Khởi tạo một hàng đợi (`Queue`) với trạng thái ban đầu là bàn cờ trống `[[]]`.
    2.  Lặp cho đến khi `Queue` rỗng:
        * Lấy trạng thái đầu tiên ra khỏi `Queue` (cơ chế FIFO - `pop(0)`).
        * Kiểm tra nếu trạng thái này là mục tiêu thì trả về kết quả.
        * Nếu không, sinh ra tất cả các trạng thái con hợp lệ (bằng cách đặt thêm một quân xe vào cột chưa có) và thêm chúng vào cuối `Queue`.
* **Kết quả sau áp dụng thuật toán**:
    ![](assets/8Rooks_Gif/BFS.gif)

#### 2. Tìm kiếm theo chiều sâu (DFS)

* **Mô tả**: Tìm kiếm theo chiều sâu ([Depth-First Search](https://vi.wikipedia.org/wiki/T%C3%ACm_ki%E1%BA%BFm_theo_chi%E1%BB%81u_s%C3%A2u)) ưu tiên đi sâu vào một nhánh của cây tìm kiếm trước khi quay lui.
* **Các bước thực hiện trong code**:
    1.  Khởi tạo một ngăn xếp (`Stack`) với trạng thái ban đầu là bàn cờ trống `[[]]`.
    2.  Lặp cho đến khi `Stack` rỗng:
        * Lấy trạng thái cuối cùng ra khỏi `Stack` (cơ chế LIFO - `pop()`).
        * Kiểm tra nếu trạng thái này là mục tiêu thì trả về kết quả.
        * Nếu không, sinh các trạng thái con hợp lệ và thêm chúng vào `Stack`. (Các trạng thái con được sinh theo thứ tự cột giảm dần để đảm bảo nhánh có cột nhỏ hơn được khám phá trước).
* **Kết quả sau áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 3. Tìm kiếm chi phí đồng đều (UCS)

* **Mô tả**: Thuật toán tìm kiếm chi phí đồng đều ([Uniform Cost Search](https://vi.wikipedia.org/wiki/T%C3%ACm_ki%E1%BA%BFm_chi_ph%C3%AD_%C4%91%E1%BB%81u)) mở rộng node có chi phí đường đi (path cost) thấp nhất từ điểm bắt đầu. Nó sử dụng hàng đợi ưu tiên (`heapq`) và đảm bảo tìm thấy lời giải có tổng chi phí thấp nhất.
* **Các bước thực hiện trong code**:
    1.  Khởi tạo một hàng đợi ưu tiên (`Queue`) chứa `(cost, state)`, với trạng thái ban đầu là `(0, ())`.
    2.  Lặp cho đến khi `Queue` rỗng:
        * Lấy ra trạng thái có `cost` thấp nhất.
        * Nếu là trạng thái mục tiêu thì dừng.
        * Nếu không, sinh các trạng thái con, tính chi phí mới (`new_cost = cost + RookCost(...)`) và đẩy `(new_cost, new_state)` vào hàng đợi ưu tiên.
* **Kết quả sau áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 4. Tìm kiếm sâu dần (IDS)

* **Mô tả**: Thuật toán tìm kiếm sâu dần ([Iterative Deepening Search](https://en.wikipedia.org/wiki/Iterative_deepening_depth-first_search)) là sự kết hợp giữa BFS và DFS, thực hiện một loạt các tìm kiếm giới hạn độ sâu (DLS) với độ sâu tăng dần.
* **Các bước thực hiện trong code**:
    1.  Thực hiện một vòng lặp với `limit` (độ sâu giới hạn) tăng từ 1 đến 8.
    2.  Trong mỗi vòng lặp, gọi thuật toán `DepthLimitedSearch` với `limit` hiện tại.
    3.  Nếu `DepthLimitedSearch` trả về một lời giải, thuật toán IDS sẽ dừng lại và trả về lời giải đó.
* **Kết quả sau áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 5. Tìm kiếm theo chiều sâu giới hạn (DLS)

* **Mô tả**: Thuật toán tìm kiếm theo chiều sâu giới hạn ([Depth-Limited Search](https://www.geeksforgeeks.org/artificial-intelligence/depth-limited-search-for-ai/)) là một biến thể của DFS, trong đó việc tìm kiếm sẽ dừng lại khi đạt đến một độ sâu giới hạn cho trước.
* **Các bước thực hiện trong code**:
    1.  Sử dụng một hàm đệ quy `Recursive_DLS(state, solution, limit)`.
    2.  Nếu trạng thái là mục tiêu, trả về trạng thái đó.
    3.  Nếu `limit` bằng 0, dừng nhánh này và trả về `None`.
    4.  Nếu không, với mỗi trạng thái con hợp lệ, gọi đệ quy `Recursive_DLS(child, solution, limit - 1)`.
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

---

### 2.2. Nhóm thuật toán tìm kiếm có thông tin (Informed Search)

#### 1. Tìm kiếm tham lam (Greedy Search)

* **Mô tả**: Thuật toán tìm kiếm tham lam ([Greedy Search](https://en.wikipedia.org/wiki/Greedy_algorithm)) luôn chọn bước đi có vẻ tốt nhất tại thời điểm hiện tại. Nó sử dụng một hàm ước lượng chi phí (heuristic) để đánh giá khoảng cách từ trạng thái hiện tại đến mục tiêu.
* **Các bước thực hiện trong code**:
    1.  Sử dụng hàng đợi ưu tiên (`heapq`) để lưu `(heuristic, state)`.
    2.  Hàm heuristic `H_Manhattan` được sử dụng để tính tổng khoảng cách Manhattan từ vị trí các quân xe hiện tại đến vị trí mục tiêu.
    3.  Tại mỗi bước, thuật toán lấy ra trạng thái có giá trị `heuristic` thấp nhất và sinh ra các trạng thái con từ đó.
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 2. Tìm kiếm A* (A\* Search)

* **Mô tả**: Thuật toán [A\* Search](https://vi.wikipedia.org/wiki/Gi%E1%BA%A3i_thu%E1%BA%ADt_t%C3%ACm_ki%E1%BA%BFm_A*) kết hợp ưu điểm của UCS và Greedy Search, đánh giá các node dựa trên hàm `f(n) = g(n) + h(n)`.
* **Các bước thực hiện trong code**:
    1.  Sử dụng hàng đợi ưu tiên (`heapq`) để lưu `(f, g, state)`.
    2.  `g(n)` là chi phí đường đi thực tế, tính bằng `RookCost`.
    3.  `h(n)` là chi phí ước lượng, tính bằng `H_Manhattan`.
    4.  Tại mỗi bước, thuật toán lấy ra trạng thái có giá trị `f` thấp nhất và sinh ra các trạng thái con từ đó.
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

---

### 2.3. Nhóm thuật toán tìm kiếm cục bộ (Local Search)

#### 1. Leo đồi (Hill Climbing)

* **Mô tả**: Thuật toán [Hill Climbing](https://en.wikipedia.org/wiki/Hill_climbing) tại mỗi bước sẽ di chuyển đến trạng thái "láng giềng" tốt hơn trạng thái hiện tại và dừng lại khi không có láng giềng nào tốt hơn.
* **Các bước thực hiện trong code**:
    1.  Bắt đầu với một trạng thái rỗng.
    2.  Lặp qua từng hàng, sinh ra tất cả các trạng thái con khả thi (bằng cách đặt một quân xe vào hàng đó).
    3.  Chọn trạng thái con có giá trị heuristic (`H_match` - số quân xe đặt đúng vị trí) cao nhất.
    4.  Nếu giá trị heuristic của trạng thái tốt nhất không cao hơn trạng thái hiện tại, thuật toán sẽ dừng lại (đạt đỉnh cục bộ).
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 2. Luyện kim mô phỏng (Simulated Annealing)

* **Mô tả**: Thuật toán [Simulated Annealing](https://en.wikipedia.org/wiki/Simulated_annealing) là một cải tiến của Hill Climbing. Thỉnh thoảng, thuật toán sẽ chấp nhận cả những nước đi "tệ hơn" với một xác suất nhất định, giúp nó thoát khỏi các đỉnh cục bộ.
* **Các bước thực hiện trong code**:
    1.  Tương tự Hill Climbing, nhưng nếu trạng thái tốt nhất không cải thiện so với hiện tại, thuật toán sẽ tính toán một xác suất `p = exp(delta / T)`.
    2.  Nó sẽ chấp nhận một nước đi tệ hơn nếu một số ngẫu nhiên nhỏ hơn `p`.
    3.  Nhiệt độ `T` sẽ giảm dần sau mỗi bước (`T *= alpha`), làm cho xác suất chấp nhận nước đi tệ giảm theo thời gian.
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 3. Tìm kiếm Beam (Beam Search)

* **Mô tả**: Thuật toán [Beam Search](https://en.wikipedia.org/wiki/Beam_search) là một biến thể của BFS nhưng chỉ giữ lại một số lượng `k` (beam width) các trạng thái tốt nhất ở mỗi mức để khám phá tiếp.
* **Các bước thực hiện trong code**:
    1.  Bắt đầu với một `beam` chứa trạng thái ban đầu.
    2.  Ở mỗi hàng, sinh ra tất cả các trạng thái con từ tất cả các trạng thái trong `beam` hiện tại.
    3.  Từ danh sách tất cả các trạng thái con vừa sinh, chọn ra `k` trạng thái tốt nhất (dựa trên `H_match`) để tạo thành `beam` cho vòng lặp tiếp theo.
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 4. Giải thuật di truyền (Genetic Algorithm)

* **Mô tả**: [Genetic Algorithm](https://aivietnam.edu.vn/blog/giai-thuat-di-truyen) mô phỏng quá trình tiến hóa tự nhiên để tìm kiếm lời giải.
* **Các bước thực hiện trong code**:
    1.  **Khởi tạo**: Tạo một quần thể ban đầu gồm các hoán vị ngẫu nhiên.
    2.  **Đánh giá**: Tính `fitness` (độ tốt) cho mỗi cá thể bằng hàm `H_match`.
    3.  **Chọn lọc**: Sử dụng `Tournament Selection` để chọn các cá thể cha mẹ.
    4.  **Lai ghép**: Tạo ra các cá thể con bằng phương pháp `Order Crossover (OX)`.
    5.  **Đột biến**: Áp dụng đột biến (hoán đổi 2 vị trí) cho các cá thể con với một xác suất nhỏ.
    6.  Lặp lại quá trình qua nhiều thế hệ, giữ lại cá thể tốt nhất ở mỗi thế hệ (elitism).
* **Kết quả sau khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

---

### 2.4. Nhóm thuật toán trong môi trường phức tạp

#### 1. Tìm kiếm And-Or (And-Or Search)

* **Mô tả**: Thuật toán [And-Or Search](https://en.wikipedia.org/wiki/And%E2%80%93or_tree) được sử dụng trong các môi trường không xác định (nondeterministic), nơi một hành động có thể dẫn đến nhiều kết quả.
* **Các bước thực hiện trong code**:
    1.  Sử dụng tìm kiếm đệ quy. Một node **OR** (đại diện cho lựa chọn hành động của agent) thành công nếu *ít nhất một* hành động dẫn đến thành công.
    2.  Một node **AND** (đại diện cho các kết quả có thể xảy ra của một hành động) thành công chỉ khi *tất cả* các kết quả đều có thể được xử lý để dẫn đến mục tiêu.
    3.  Sử dụng memoization để lưu kết quả các bài toán con và phát hiện chu trình để tránh lặp vô hạn.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 2. Tìm kiếm trong môi trường không quan sát được (Unobservable)

* **Mô tả**: Agent không biết trạng thái hiện tại của nó mà duy trì một "tập niềm tin" (belief state) - là tập hợp tất cả các trạng thái có thể có.
* **Các bước thực hiện trong code**:
    1.  Bắt đầu với một `start_belief` bao gồm trạng thái rỗng và các trạng thái có 1 quân cờ.
    2.  Sử dụng DFS để tìm kiếm trên không gian của các `belief state`.
    3.  Các hành động `update_belief_place` (đã được ngẫu nhiên hóa) và `update_belief_move` được áp dụng cho toàn bộ `belief` để tạo ra `belief` mới.
    4.  Điều kiện mục tiêu (`is_goal_belief`) là khi **tất cả** các `state` trong `belief` hiện tại đều là một lời giải 8-quân hợp lệ.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 3. Tìm kiếm trong môi trường quan sát được một phần (Partially Observable)

* **Mô tả**: Đây là trường hợp tổng quát hơn, nơi agent có một số thông tin nhưng không đủ để xác định chính xác trạng thái hiện tại.
* **Các bước thực hiện trong code**:
    1.  `start_belief` được tạo ra dựa trên một phần của lời giải đã biết (`k` quân cờ đầu tiên) và thêm vào một vài biến thể ngẫu nhiên.
    2.  `goal_beliefs` cũng là một tập hợp các lời giải có chung `k` quân cờ đầu tiên.
    3.  Thuật toán sử dụng DFS để tìm kiếm một `belief` mà trong đó, **tất cả** các `state` đều là thành viên của `goal_beliefs`.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

---

### 2.5. Nhóm thuật toán Thỏa mãn ràng buộc (Constraint Satisfaction Problem)

#### 1. Quay lui (Backtracking)

* **Mô tả**: [Backtracking](https://en.wikipedia.org/wiki/Backtracking) là thuật toán cơ bản cho CSP. Nó gán giá trị cho các biến một cách tuần tự và quay lui khi vi phạm ràng buộc.
* **Các bước thực hiện trong code**:
    1.  Sử dụng hàm đệ quy `Backtrack(state)`.
    2.  Tại mỗi hàng, thử đặt quân xe vào các cột khả thi (những cột chưa được sử dụng).
    3.  Nếu một cột được chọn, gọi đệ quy cho hàng tiếp theo.
    4.  Nếu lời gọi đệ quy không tìm được lời giải, "quay lui" bằng cách xóa quân xe vừa đặt (`state.pop()`) và thử cột khác.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 2. Kiểm tra phía trước (Forward Checking)

* **Mô tả**: Đây là một cải tiến của Backtracking. Mỗi khi gán một giá trị, nó sẽ "kiểm tra phía trước" và tạm thời loại bỏ các giá trị không tương thích khỏi miền của các biến chưa được gán.
* **Các bước thực hiện trong code**:
    1.  Sử dụng hàm đệ quy `FC_Backtrack(state, domains)`.
    2.  Khi đặt một quân xe ở `(hàng, cột)`, thuật toán sẽ loại bỏ `cột` đó khỏi `domains` của tất cả các `hàng` tương lai.
    3.  Nếu bất kỳ `domain` nào của hàng tương lai trở nên rỗng, nhánh tìm kiếm này thất bại.
    4.  Sau khi quay lui, các giá trị đã loại bỏ sẽ được khôi phục lại vào `domains`.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

#### 3. Thuật toán AC-3 (Arc Consistency)

* **Mô tả**: Thuật toán [AC-3](https://en.wikipedia.org/wiki/AC-3_algorithm) được sử dụng để tiền xử lý bài toán CSP, loại bỏ các giá trị không nhất quán khỏi miền giá trị của các biến trước khi bắt đầu tìm kiếm.
* **Các bước thực hiện trong code**:
    1.  **Tiền xử lý AC-3**: Xây dựng một hàng đợi chứa tất cả các "cung" `(hàng_i, hàng_j)`. Lặp và loại bỏ các giá trị không nhất quán khỏi miền của `hàng_i` dựa trên miền của `hàng_j` cho đến khi không còn gì để loại bỏ.
    2.  **Tìm kiếm**: Sau khi các miền giá trị đã được thu hẹp, gọi thuật toán `backtrack` tiêu chuẩn trên các miền đã được tối ưu hóa này.
* **Kết quả khi áp dụng thuật toán**:
    *(Chèn ảnh GIF của bạn ở đây)*

## 3. Môi trường phát triển

* **Ngôn ngữ**: Python 3.10+
* **Thư viện chính**:
    * `pygame`: Để xây dựng toàn bộ giao diện đồ họa và xử lý sự kiện.
    * `Pillow` (PIL): Để xử lý và hiển thị hình ảnh quân cờ.
* **Cài đặt thư viện**:
    ```bash
    pip install pygame
    pip install Pillow
    ```

## 4. Hướng dẫn sử dụng chương trình

1.  **Chạy chương trình**:
    Thực thi file `main.py` (hoặc file chính chứa vòng lặp game của bạn) để khởi chạy ứng dụng.
    ```bash
    python main.py
    ```

2.  **Giao diện chính**:
    Chương trình sẽ hiển thị giao diện chính bao gồm các thành phần sau:
    * **Bên trái**: Bảng điều khiển để chọn thuật toán.
    * **Ở giữa**: Hai bàn cờ 8x8, một cho trạng thái bắt đầu (trống) và một cho trạng thái mục tiêu (được tạo ngẫu nhiên).
    * **Bên phải**: Bảng thông tin hiển thị trạng thái và lịch sử các lần chạy.
    * **Phía dưới**: Các nút điều khiển chính.

3.  **Chọn thuật toán**:
    * Nhấp vào một trong 5 **nhóm thuật toán** ở cột bên trái (ví dụ: "Uninformed Search").
    * Một danh sách các thuật toán cụ thể thuộc nhóm đó sẽ hiện ra bên dưới.
    * Nhấp vào thuật toán bạn muốn chạy (ví dụ: "DFS").

4.  **Chạy và Trực quan hóa**:
    * Nhấn nút **`Start`**: Thuật toán sẽ chạy và chỉ hiển thị các bước của lời giải cuối cùng.
    * Nhấn nút **`Visualize`**: Thuật toán sẽ chạy và hiển thị toàn bộ quá trình tìm kiếm, bao gồm cả những nhánh sai.
    * Nhấn nút **`Stop`**: Dừng quá trình trực quan hóa đang diễn ra.

5.  **Các chức năng khác**:
    * **`Random Solution`**: Tạo một trạng thái mục tiêu mới một cách ngẫu nhiên.
    * **`Statistics`**: Sau khi chạy ít nhất một thuật toán, nhấn nút này để mở bảng thống kê chi tiết, so sánh hiệu suất giữa các thuật toán đã chạy thông qua bảng số liệu và biểu đồ trực quan.

## 5. Cấu trúc dự án

Dự án được tổ chức theo cấu trúc gần với mô hình MVC (Model-View-Controller) để dễ quản lý và mở rộng:

* **Model**: Thư mục `algorithms/` chứa logic của tất cả các thuật toán tìm kiếm. Đây là "bộ não" của ứng dụng, xử lý việc tìm kiếm lời giải. Thư mục `engine/` chứa các lớp hỗ trợ như `PerformanceTracker`.
* **View**: File `gui/renderer.py` chịu trách nhiệm vẽ toàn bộ các thành phần giao diện người dùng, từ bàn cờ, các nút bấm cho đến bảng thống kê.
* **Controller**: File `gui/game_8Rooks.py` đóng vai trò là bộ điều khiển trung tâm, xử lý các sự kiện đầu vào của người dùng (click chuột, cuộn), gọi các thuật toán tương ứng từ Model, và ra lệnh cho View cập nhật lại giao diện.
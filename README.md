# 2021l_INT3401_8_Pacman_Multiagents
Solutions for Pacman projects problems - Multiagents problems

Câu hỏi 1: Thiết kế hàm đánh giá trạng thái cho reflex Agent:
Hàm trả về kết quả của biến score - điểm số đánh giá trạng thái. 2 yếu tố ảnh hưởng đến kết quả này là khoảng cách từ pacman đến thức ăn và khoảng cách từ Pacman đến đối thủ (các con ma). Khoảng cách đến thức ăn càng xa thì điểm số sẽ càng thấp. Khoảng cách đến ma càng gần thì số điểm sẽ bị trừ nhiều hơn.

Câu hỏi 2: Thiết kế hàm getAction() của Minimax Agent:
Sẽ có 2 hàm được cài đặt bên trong getAction() là hàm maxValue() và minValue(). Hàm maxValue() trả về kết quả tốt nhất kèm với action tương ứng trong số các kết quả thu được qua lệnh gọi đệ quy hàm minLevel(). Hàm minValue() tương tự như maxValue() nhưng để lấy kết quả cho tác tử Ma. Kết quả trả về cuối cùng sẽ là hành động có kết quả tốt nhất đối với trạng thái hiện tại của Pacman.

Câu hỏi 3: Thiết kế hàm getAction() của AlphaBeta Agent:
Cách thiết kế tương tự với getAction() của Minimax Agent. Tuy nhiên có sự tham gia của 2 tham số alpha và beta để tăng hiệu suất cho thuật toán, giảm thiểu số lần gọi hàm đệ quy. Cài đặt của thuật toán tương tự như đã được trình bày trong slide bài giảng.

Câu hỏi 4: Thiết kế hàm getAction() của Expectimax Agent:
Khác với Minimax Agent thì Expectimax Agent sẽ giả định là các tác tử Ma không phải lúc nào cũng chọn lựa chọn tốt nhất để gây bất lợi cho Pacman. Cách cài đặt sẽ hơi khác so với getAction() của Minimax 1 chút tuy nhiên hàm maxLevel() vẫn giữ nguyên. Hàm minLevel() sẽ đổi tên thành expectLevel(). Giá trị trả về của những lần đệ quy hàm expectLevel() - theo mình lựa chọn - sẽ là giá trị trung bình (tổng giá trị trả về của các hàm / số action của tác tử Ma).

Câu hỏi 5: Cải thiện hàm đánh giá (betterEvaluationFunction()):
Cách thiết kế không khác nhiều so với yêu cầu của câu hỏi đầu tiên. Điểm khác là sẽ có thêm yếu tố "viên nhộng" là loại thức ăn đặc biệt mà khi Pacman ăn được sẽ làm tác tử Ma rơi vào trạng thái "Sợ". Và Pacman có thể tiêu diệt được những ma đang ở trong trạng thái này.





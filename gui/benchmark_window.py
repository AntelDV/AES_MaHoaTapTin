import customtkinter as ctk
import tkinter as tk
import threading 
import os
from queue import Queue 
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from data.benchmark import run_benchmark_logic

class BenchmarkWindow(ctk.CTkToplevel):
    """
    Cửa sổ popup để chạy Benchmark trên 1 file và hiển thị kết quả.
    """
    def __init__(self, master, input_filepath: str):
        super().__init__(master)
        self.title("Phân tích Hiệu năng (Benchmark)")
        self.geometry("800x600")
        self.minsize(700, 500)
        
        # Lưu file đầu vào
        self.input_filepath = input_filepath
        
        self.after(100, self.grab_set) 

        self.results = None
        self.is_running = False
        
        # --- Cấu hình Grid ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        
        # --- Nút Bắt đầu/Dừng ---
        self.start_button = ctk.CTkButton(
            self, 
            text=f"Bắt đầu Phân tích (File: {os.path.basename(self.input_filepath)})", 
            command=self.toggle_benchmark,
            height=40
        )
        self.start_button.grid(row=0, column=0, padx=20, pady=20, sticky="ew")

        # --- Tab (Log và Đồ thị) ---
        self.tab_view = ctk.CTkTabview(self, anchor="w")
        self.tab_view.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        self.tab_log = self.tab_view.add("Log (Kết quả Text)")
        self.tab_chart = self.tab_view.add("Đồ thị So sánh") 
        
        # --- Tab Log ---
        self.log_textbox = ctk.CTkTextbox(
            self.tab_log, 
            state="disabled", 
            font=ctk.CTkFont(family="monospace", size=12)
        )
        self.log_textbox.pack(fill="both", expand=True, padx=5, pady=5)

        # --- Tab Đồ thị  ---
        self.chart_frame = ctk.CTkFrame(self.tab_chart, fg_color="white")
        self.chart_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.log_queue = Queue()
        self.after(100, self.process_log_queue)

    def add_log(self, message):
        self.log_queue.put(message)

    def process_log_queue(self):
        while not self.log_queue.empty():
            message = self.log_queue.get_nowait()
            if message:
                self.log_textbox.configure(state="normal")
                self.log_textbox.insert("end", message + "\n")
                self.log_textbox.configure(state="disabled")
                self.log_textbox.see("end")
        self.after(100, self.process_log_queue)

    def toggle_benchmark(self):
        if not self.is_running:
            self.is_running = True
            self.start_button.configure(text="Đang chạy... Vui lòng chờ...", state="disabled")
            self.log_textbox.configure(state="normal")
            self.log_textbox.delete("1.0", "end")
            self.log_textbox.configure(state="disabled")
            
            for widget in self.chart_frame.winfo_children():
                widget.destroy()
            
            threading.Thread(target=self.run_benchmark_thread, daemon=True).start()

    def run_benchmark_thread(self):
        """Hàm này chạy trong luồng riêng."""
        # Chạy logic với file đã chọn
        self.results = run_benchmark_logic(self.input_filepath, log_callback=self.add_log)
        self.after(0, self.on_benchmark_complete)

    def on_benchmark_complete(self):
        """Hàm này chạy trong luồng GUI khi benchmark xong."""
        self.is_running = False
        self.start_button.configure(text=f"Bắt đầu Phân tích (File: {os.path.basename(self.input_filepath)})", state="normal")
        
        if self.results:
            self.add_log("\n--- HOÀN TẤT: Đang vẽ biểu đồ cột ---")
            try:
                self.draw_bar_chart(self.chart_frame, self.results)
                self.add_log("Vẽ đồ thị thành công. Chuyển qua tab 'Đồ thị' để xem.")
            except Exception as e:
                self.add_log(f"Lỗi khi vẽ đồ thị: {e}")
        else:
            self.add_log("Không có kết quả để vẽ đồ thị.")
            
    def draw_bar_chart(self, frame, results):
        """Vẽ BIỂU ĐỒ CỘT (Bar Chart) vào 1 CTkFrame."""
        
        # Chuẩn bị dữ liệu
        key_names = [r['key_name'] for r in results]
        encrypt_times = [r['encrypt_time'] for r in results]
        decrypt_times = [r['decrypt_time'] for r in results]
        
        if not key_names:
            self.add_log("Lỗi dữ liệu đồ thị: Không có dữ liệu.")
            return

        # Cấu hình Matplotlib
        fig = Figure(figsize=(7, 5), dpi=100)
        
        # --- Biểu đồ 1: Mã hóa ---
        ax1 = fig.add_subplot(211) # 2 hàng, 1 cột, vị trí 1
        bars_enc = ax1.bar(key_names, encrypt_times, color=['#61AFEF', '#C678DD', '#E06C75'])
        ax1.set_title(f'Thời gian Mã hóa (File: {os.path.basename(self.input_filepath)})')
        ax1.set_ylabel('Thời gian (giây)')
        ax1.grid(axis='y', linestyle='--', alpha=0.7)
        # Thêm nhãn số liệu
        ax1.bar_label(bars_enc, fmt='%.3fs')

        # --- Biểu đồ 2: Giải mã ---
        ax2 = fig.add_subplot(212) # 2 hàng, 1 cột, vị trí 2
        bars_dec = ax2.bar(key_names, decrypt_times, color=['#61AFEF', '#C678DD', '#E06C75'])
        ax2.set_title(f'Thời gian Giải mã (File: {os.path.basename(self.input_filepath)})')
        ax2.set_ylabel('Thời gian (giây)')
        ax2.grid(axis='y', linestyle='--', alpha=0.7)
        ax2.bar_label(bars_dec, fmt='%.3fs')
        
        fig.tight_layout() 
        
        # Nhúng vào Tkinter
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
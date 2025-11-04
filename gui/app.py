import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog
from core.file_handler import encrypt_file, decrypt_file, FileHandlerError
from gui.benchmark_window import BenchmarkWindow

STATUS_COLORS = {
    "default": ("#DADADA", "#E0E0E0"),
    "blue":    ("#1F6AA5", "#61AFEF"),
    "green":   ("#097954", "#98C379"),
    "orange":  ("#B45309", "#D19A66"),
    "red":     ("#B91C1C", "#E06C75")
}

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Đề tài 18 - Ứng dụng AES để bảo mật tập tin văn bản ")
        self.geometry("600x480")
        self.minsize(550, 450)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_rowconfigure(1, weight=1) 
        self.grid_rowconfigure(2, weight=1) 
        self.grid_rowconfigure(3, weight=1) 
        self.grid_rowconfigure(4, weight=2) 
        self.input_file_path = tk.StringVar()
        self.key_strength = tk.StringVar(value="AES-128 (16 ký tự)")
        self.status_message = tk.StringVar()
        self.benchmark_popup = None
        self._create_widgets()
        self._update_status("Chào mừng! Vui lòng chọn file và cấu hình khóa.", "default")

    def _create_widgets(self):
        # --- 0. Khung Tiêu đề và Nút Benchmark ---
        title_frame = ctk.CTkFrame(self, fg_color="transparent")
        title_frame.grid(row=0, column=0, padx=20, pady=(15, 0), sticky="ew")
        title_frame.grid_columnconfigure(0, weight=1)
        self.benchmark_button = ctk.CTkButton(
            title_frame,
            text="📊 Phân tích Hiệu năng",
            command=self.open_benchmark_window,
            width=120,
            fg_color="#3a3a3a",
            hover_color="#454545"
        )
        self.benchmark_button.grid(row=0, column=1, sticky="e")

        # --- 1. Khung chọn File ---
        file_frame = ctk.CTkFrame(self, corner_radius=10)
        file_frame.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="new")
        file_frame.grid_columnconfigure(1, weight=1)
        file_label = ctk.CTkLabel(file_frame, text="1. File Đầu Vào:", font=ctk.CTkFont(weight="bold"))
        file_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        self.file_entry = ctk.CTkEntry(
            file_frame, textvariable=self.input_file_path, state="readonly"
        )
        self.file_entry.grid(row=0, column=1, padx=(0, 15), pady=15, sticky="ew")
        self.file_button = ctk.CTkButton(
            file_frame, text="📂", command=self._browse_file, 
            width=50, font=ctk.CTkFont(size=20)
        )
        self.file_button.grid(row=0, column=2, padx=(0, 15), pady=15, sticky="e")

        # --- 2. Khung nhập Khóa ---
        key_frame = ctk.CTkFrame(self, corner_radius=10)
        key_frame.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        key_frame.grid_columnconfigure(1, weight=1)
        key_config_label = ctk.CTkLabel(key_frame, text="2. Cấu hình Khóa:", font=ctk.CTkFont(weight="bold"))
        key_config_label.grid(row=0, column=0, columnspan=2, padx=15, pady=(15, 10), sticky="w")
        strength_label = ctk.CTkLabel(key_frame, text="Độ mạnh:")
        strength_label.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="w")
        strength_combo = ctk.CTkComboBox(
            key_frame,
            variable=self.key_strength,
            values=["AES-128 (16 ký tự)", "AES-192 (24 ký tự)", "AES-256 (32 ký tự)"],
            state="readonly"
        )
        strength_combo.grid(row=1, column=1, columnspan=2, padx=15, pady=(5, 15), sticky="ew")
        key_label = ctk.CTkLabel(key_frame, text="Nhập khóa:")
        key_label.grid(row=2, column=0, padx=15, pady=(5, 20), sticky="w")
        self.key_entry = ctk.CTkEntry(key_frame, show="*")
        self.key_entry.grid(row=2, column=1, columnspan=2, padx=15, pady=(5, 20), sticky="ew")

        # --- 3. Khung Nút Chức Năng ---
        action_frame = ctk.CTkFrame(self, fg_color="transparent")
        action_frame.grid(row=3, column=0, padx=20, pady=10, sticky="ew")
        action_frame.grid_columnconfigure(0, weight=1)
        action_frame.grid_columnconfigure(1, weight=1)
        encrypt_button = ctk.CTkButton(
            action_frame, text="Mã Hóa", command=self._encrypt_action, 
            height=40, font=ctk.CTkFont(size=14, weight="bold")
        )
        encrypt_button.grid(row=0, column=0, padx=(0, 10), sticky="ew")
        decrypt_button = ctk.CTkButton(
            action_frame, text="Giải Mã", command=self._decrypt_action,
            height=40, font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#D19A66", hover_color="#B45309"
        )
        decrypt_button.grid(row=0, column=1, padx=(10, 0), sticky="ew")

        # --- 4. Khung Trạng Thái ---
        status_frame_container = ctk.CTkFrame(self, corner_radius=10)
        status_frame_container.grid(row=4, column=0, padx=20, pady=(10, 20), sticky="nsew")
        status_frame_container.grid_rowconfigure(1, weight=1)
        status_frame_container.grid_columnconfigure(0, weight=1)
        status_title = ctk.CTkLabel(status_frame_container, text="Trạng Thái", font=ctk.CTkFont(weight="bold"))
        status_title.grid(row=0, column=0, padx=15, pady=(10, 5), sticky="w")
        self.status_label = ctk.CTkLabel(
            status_frame_container, textvariable=self.status_message,
            wraplength=500, anchor="nw", justify="left", font=ctk.CTkFont(size=13)
        )
        self.status_label.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="nsew")
        self.status_label.bind("<Configure>", self._on_resize_status)

    def _on_resize_status(self, event):
        self.status_label.configure(wraplength=event.width - 30)

    def _browse_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.input_file_path.set(file_path)
            self._update_status(f"Đã chọn file: {file_path}", "blue")

    def _run_action(self, mode: str):
        input_file = self.input_file_path.get()
        key = self.key_entry.get()
        strength_selection = self.key_strength.get()
        
        if not input_file:
            self._update_status("Lỗi: Vui lòng chọn file đầu vào.", "red")
            return
            
        try:
            key_bytes = key.encode('utf-8')
            key_len = len(key_bytes)
        except UnicodeEncodeError:
            self._update_status("Lỗi: Khóa chứa ký tự không hợp lệ.", "red")
            return
            
        required_len = 0
        if strength_selection.startswith("AES-128"): required_len = 16
        elif strength_selection.startswith("AES-192"): required_len = 24
        elif strength_selection.startswith("AES-256"): required_len = 32
        
        if key_len != required_len:
            self._update_status(
                f"Lỗi: Bạn chọn {strength_selection}, nhưng khóa bạn nhập có {key_len} bytes (yêu cầu {required_len} bytes).", 
                "red"
            )
            return

        if mode == "encrypt":
            output_file = filedialog.asksaveasfilename(
                title="Lưu file đã mã hóa",
                defaultextension=".enc",
                filetypes=[("Encrypted files", "*.enc"), ("All files", "*.*")]
            )
        else:
             output_file = filedialog.asksaveasfilename(
                title="Lưu file đã giải mã",
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
        
        if not output_file:
            self._update_status("Hành động đã bị hủy.", "orange")
            return

        try:
            action_text = "Mã hóa" if mode == "encrypt" else "Giải mã"
            self._update_status(f"Đang {action_text}... Vui lòng chờ.", "blue")
            self.update_idletasks()
            
            if mode == "encrypt":
                encrypt_file(input_file, output_file, key)
            else:
                decrypt_file(input_file, output_file, key)
                
            self._update_status(f"{action_text} thành công! Đã lưu tại:\n{output_file}", "green")
        
        except FileHandlerError as e:
            self._update_status(f"Lỗi: {e}", "red")
        except Exception as e:
            self.update_idletasks()
            self._update_status(f"Lỗi hệ thống không lường trước: {e}", "red")

    def _encrypt_action(self):
        self._run_action(mode="encrypt")

    def _decrypt_action(self):
        self._run_action(mode="decrypt")

    def _update_status(self, message: str, color_key: str):
        self.status_message.set(message)
        color = STATUS_COLORS.get(color_key, STATUS_COLORS["default"])
        self.status_label.configure(text_color=color)
    
    def open_benchmark_window(self):
        """
        Mở cửa sổ popup Benchmark.
        """        
        # 1. Kiểm tra xem đã chọn file chưa
        current_file = self.input_file_path.get()
        if not current_file:
            self._update_status("Lỗi: Vui lòng chọn 1 file ở mục [1] trước khi phân tích.", "red")
            return
            
        # 2. Kiểm tra xem cửa sổ đã mở chưa
        if (self.benchmark_popup is None or 
            not self.benchmark_popup.winfo_exists()):
            
            # 3. Truyền file đã chọn vào popup
            self.benchmark_popup = BenchmarkWindow(self, input_filepath=current_file) 
            self.benchmark_popup.focus()
        else:
            self.benchmark_popup.focus()
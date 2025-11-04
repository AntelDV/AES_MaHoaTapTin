import os
import sys
import time
import shutil

# --- Cấu hình Path ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(SCRIPT_DIR)
sys.path.append(PARENT_DIR)

try:
    from core.file_handler import encrypt_file, decrypt_file
except ImportError:
    print("Lỗi: Không thể import 'core.file_handler'.")
    sys.exit(1)



# Thư mục chứa file TẠM (VD: temp_file.enc, temp_file.dec)
OUTPUT_DIR = os.path.join(SCRIPT_DIR, "temp_benchmark_output")
KEYS = {
    "AES-128": "0123456789abcde!", # 16 bytes
    "AES-192": "0123456789abcdef01234567", # 24 bytes
    "AES-256": "0123456789abcdef0123456789abcdef" # 32 bytes
}

# --- Các hàm trợ giúp  ---
def setup_output_dir():
    """Tạo thư mục output SẠCH."""
    if os.path.exists(OUTPUT_DIR):
        shutil.rmtree(OUTPUT_DIR)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

def cleanup_output_dir(log_callback=print):
    """Dọn dẹp thư mục output."""
    try:
        if os.path.exists(OUTPUT_DIR):
            shutil.rmtree(OUTPUT_DIR)
        log_callback(f"\nĐã dọn dẹp thư mục tạm: {OUTPUT_DIR}")
    except Exception as e:
        log_callback(f"Lỗi khi dọn dẹp thư mục tạm: {e}")

def run_benchmark_logic(input_filepath: str, log_callback=print):
    """
    Chạy logic benchmark trên 1 cùng 1 file và trả về kết quả.
    """
    results_list = [] 
    
    if not os.path.exists(input_filepath):
        log_callback(f"Lỗi: Không tìm thấy file đầu vào: {input_filepath}")
        return None

    try:
        setup_output_dir()
        
        file_size = os.path.getsize(input_filepath)
        size_label = f"{file_size / (1024*1024):.2f} MB"
        
        log_callback(f"--- Bắt đầu phân tích file: {os.path.basename(input_filepath)} ({size_label}) ---")
        
        header = f"{'Phiên bản':<10} | {'Mã hóa (s)':<20} | {'Giải mã (s)':<20}"
        log_callback("="*55)
        log_callback(header)
        log_callback("-"*55)

        for key_name, key_string in KEYS.items():
            
            # Chúng ta chỉ dùng 1 file tạm
            enc_file = os.path.join(OUTPUT_DIR, "temp.enc")
            dec_file = os.path.join(OUTPUT_DIR, "temp.dec")
            
            try:
                # --- Đo thời gian Mã hóa ---
                start_time_enc = time.time()
                encrypt_file(input_filepath, enc_file, key_string)
                time_enc = time.time() - start_time_enc
                
                # --- Đo thời gian Giải mã ---
                start_time_dec = time.time()
                decrypt_file(enc_file, dec_file, key_string)
                time_dec = time.time() - start_time_dec
                
                log_line = f"{key_name:<10} | {time_enc:<20.4f} | {time_dec:<20.4f}"
                log_callback(log_line)

                # Thêm kết quả vào list để trả về
                results_list.append({
                    "key_name": key_name,
                    "encrypt_time": time_enc,
                    "decrypt_time": time_dec
                })

            except Exception as e:
                log_callback(f"Lỗi khi xử lý với {key_name}: {e}")
        
        log_callback("-"*55)

    except Exception as e:
        log_callback(f"Lỗi nghiêm trọng trong quá trình benchmark: {e}")
    finally:
        cleanup_output_dir(log_callback=log_callback)
        log_callback("Phân tích hoàn tất!")
        
    return results_list 
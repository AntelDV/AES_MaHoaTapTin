import os
from .aes_cipher import AESCipher
from .padding import pad_pkcs7, unpad_pkcs7, PaddingError, BLOCK_SIZE

class FileHandlerError(Exception):
    """Lỗi tùy chỉnh cho các vấn đề trong quá trình xử lý file."""
    pass

def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """Hàm trợ giúp: Thực hiện phép XOR trên hai chuỗi bytes."""
    if len(a) != len(b):
        raise ValueError("Chỉ có thể XOR các chuỗi bytes có cùng độ dài.")
    
    # Dùng list comprehension để XOR từng byte và tạo list các số nguyên
    xor_result_int = [byte_a ^ byte_b for byte_a, byte_b in zip(a, b)]
    
    # Chuyển list số nguyên về lại dạng bytes
    return bytes(xor_result_int)

def encrypt_file(input_filepath: str, output_filepath: str, key_string: str):
    """
    Mã hóa một file sử dụng AES-CBC với IV ngẫu nhiên và đệm PKCS#7.
    Cấu trúc file đầu ra (.enc):
    [ 16 byte IV ] + [ Dữ liệu đã mã hóa (Ciphertext) ]
    
    Args:
        input_filepath: Đường dẫn đến file văn bản cần mã hóa.
        output_filepath: Đường dẫn đến file .enc (đầu ra).
        key_string: Khóa (dạng chuỗi) có độ dài 16, 24, hoặc 32 ký tự.
    """
    try:
        
        # Chuyển đổi khóa và khởi tạo AESCipher
        key_bytes = key_string.encode('utf-8') 
        cipher = AESCipher(key_bytes) 
        
        # Tạo IV (Initialization Vector) 16 byte ngẫu nhiên
        iv = os.urandom(BLOCK_SIZE) 
        
        # Khởi tạo giá trị ciphertext của khối trước đó (ban đầu là IV)
        previous_ciphertext_block = iv 
        
        # Mở file đọc (input) và file ghi (output)
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            
            # GHI 16 byte IV vào đầu file output
            f_out.write(iv)
            
            while True:
                #  Đọc từng khối 16 byte
                plaintext_block = f_in.read(BLOCK_SIZE) 

                if len(plaintext_block) == 16:
                    block_to_encrypt = _xor_bytes(plaintext_block, previous_ciphertext_block)
                    ciphertext_block = cipher.encrypt_block(block_to_encrypt)
                    f_out.write(ciphertext_block)
                    previous_ciphertext_block = ciphertext_block
                
                else:
                    # Đây là khối cuối cùng
                    # Áp dụng padding PKCS#7
                    # Nếu len=2, thêm 14 byte
                    # Nếu len=0, thêm 16 byte 
                    padded_block = pad_pkcs7(plaintext_block, BLOCK_SIZE) 
                    block_to_encrypt = _xor_bytes(padded_block, previous_ciphertext_block)
                    ciphertext_block = cipher.encrypt_block(block_to_encrypt)
                    f_out.write(ciphertext_block)
                    break 
                
    except ValueError as e:
        raise FileHandlerError(f"Lỗi khởi tạo AES: {e}")
    except FileNotFoundError:
        raise FileHandlerError(f"Lỗi: Không tìm thấy file đầu vào '{input_filepath}'")
    except Exception as e:
        raise FileHandlerError(f"Một lỗi đã xảy ra trong quá trình mã hóa: {e}")



def decrypt_file(input_filepath: str, output_filepath: str, key_string: str):
    """
    Giải mã một file .enc (đã được mã hóa bởi hàm encrypt_file).
    Tự động đọc IV từ đầu file, giải mã CBC, và gỡ bỏ đệm PKCS#7.

    Args:
        input_filepath: Đường dẫn đến file .enc cần giải mã.
        output_filepath: Đường dẫn đến file văn bản (đầu ra).
        key_string: Khóa (dạng chuỗi) đã dùng để mã hóa.
    """
    try:
        
        #  Chuyển đổi khóa và khởi tạo AESCipher
        key_bytes = key_string.encode('utf-8')
        cipher = AESCipher(key_bytes)

        # Mở file đọc (input) và file ghi (output)
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            # ĐỌC 16 byte ĐẦU TIÊN để lấy IV 
            iv = f_in.read(BLOCK_SIZE)
            
            if len(iv) < BLOCK_SIZE:
                raise FileHandlerError("File quá nhỏ hoặc bị hỏng, không chứa IV.")
            
            # Khởi tạo giá trị ciphertext của khối trước đó (ban đầu là IV)
            previous_ciphertext_block = iv 
            
            # Đọc khối đầu tiên của dữ liệu
            current_ciphertext_block = f_in.read(BLOCK_SIZE) 
            
            while True:
                # Đọc khối tiếp theo
                next_ciphertext_block = f_in.read(BLOCK_SIZE)
                
                if not next_ciphertext_block:
                    if not current_ciphertext_block:
                        break
                    
                    if len(current_ciphertext_block) != BLOCK_SIZE:
                         raise FileHandlerError("File bị hỏng (khối cuối không đủ 16 byte).")
                     
                    # Giải mã khối cuối
                    decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                    
                    # Hiện thực logic CBC (Giải mã)
                    plaintext_block = _xor_bytes(decrypted_block, previous_ciphertext_block)
                    
                    # Gỡ bỏ đệm PKCS#7 cho khối cuối cùng 
                    try:
                        unpadded_block = unpad_pkcs7(plaintext_block, BLOCK_SIZE)
                    except PaddingError as e:
                        raise FileHandlerError(f"Lỗi gỡ đệm. Rất có thể bạn đã nhập sai khóa. Chi tiết: {e}")
                    
                    f_out.write(unpadded_block)
                    break
                
                #  Nếu khối 'next' tồn tại 
                if len(current_ciphertext_block) != BLOCK_SIZE:
                    raise FileHandlerError("File bị hỏng (khối dữ liệu không đủ 16 byte).")
                
                # Giải mã khối 'current'
                decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                plaintext_block = _xor_bytes(decrypted_block, previous_ciphertext_block)
                f_out.write(plaintext_block)
                
                previous_ciphertext_block = current_ciphertext_block
                current_ciphertext_block = next_ciphertext_block

    except ValueError as e:
        raise FileHandlerError(f"Lỗi khởi tạo AES: {e}")
    except FileNotFoundError:
        raise FileHandlerError(f"Lỗi: Không tìm thấy file đầu vào '{input_filepath}'")
    except Exception as e:
        if not isinstance(e, FileHandlerError):
            raise FileHandlerError(f"Một lỗi đã xảy ra trong quá trình giải mã: {e}")
        else:
            raise e

# --- HÀM BỔ TRỢ ĐỂ GIẢI MÃ VÀO BỘ NHỚ ---
def decrypt_to_memory(input_filepath: str, key_string: str) -> bytes:
    """
    Giải mã file vào bộ nhớ (bytes).
    Sẽ ném ra lỗi (FileHandlerError) nếu khóa sai, trước khi lưu.
    """
    try:
        key_bytes = key_string.encode('utf-8')
        cipher = AESCipher(key_bytes)
        
        # Nơi lưu kết quả giải mã
        decrypted_data = bytearray()

        with open(input_filepath, 'rb') as f_in:
            iv = f_in.read(BLOCK_SIZE)
            if len(iv) < BLOCK_SIZE:
                raise FileHandlerError("File quá nhỏ, không chứa IV.")
            
            previous_ciphertext_block = iv
            current_ciphertext_block = f_in.read(BLOCK_SIZE)
            
            while True:
                next_ciphertext_block = f_in.read(BLOCK_SIZE)
                
                if not next_ciphertext_block: # Đây là khối cuối
                    if not current_ciphertext_block:
                        break 
                    if len(current_ciphertext_block) != BLOCK_SIZE:
                         raise FileHandlerError("File bị hỏng (khối cuối không đủ).")

                    decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                    plaintext_block = _xor_bytes(decrypted_block, previous_ciphertext_block)
                    
                    # Gỡ đệm khối cuối cùng
                    try:
                        unpadded_block = unpad_pkcs7(plaintext_block, BLOCK_SIZE)
                        decrypted_data.extend(unpadded_block)
                    except PaddingError as e:
                        raise FileHandlerError(f"Lỗi gỡ đệm. Rất có thể bạn đã nhập sai khóa. Chi tiết: {e}")
                    
                    break 
                
                # Đây KHÔNG phải khối cuối
                if len(current_ciphertext_block) != BLOCK_SIZE:
                    raise FileHandlerError("File bị hỏng (khối dữ liệu không đủ).")
                
                decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                plaintext_block = _xor_bytes(decrypted_block, previous_ciphertext_block)
                decrypted_data.extend(plaintext_block)
                
                previous_ciphertext_block = current_ciphertext_block
                current_ciphertext_block = next_ciphertext_block
        
        return bytes(decrypted_data) 

    except ValueError as e: 
        raise FileHandlerError(f"Lỗi khởi tạo AES: {e}")
    except FileNotFoundError:
        raise FileHandlerError(f"Lỗi: Không tìm thấy file đầu vào '{input_filepath}'")
    except FileHandlerError as e:
        raise e
    except Exception as e:
        raise FileHandlerError(f"Một lỗi đã xảy ra trong quá trình giải mã: {e}")
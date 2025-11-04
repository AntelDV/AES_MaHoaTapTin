import os
from .aes_cipher import AESCipher
from .padding import pad_pkcs7, unpad_pkcs7, PaddingError, BLOCK_SIZE

class FileHandlerError(Exception):
    """Lỗi tùy chỉnh cho các vấn đề trong quá trình xử lý file."""
    pass

def _xor_bytes(a: bytes, b: bytes) -> bytes:
    """
    Hàm trợ giúp: Thực hiện phép XOR trên hai chuỗi bytes.
    Yêu cầu: len(a) == len(b).
    """
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
        # 1. Chuyển đổi khóa và khởi tạo AESCipher
        key_bytes = key_string.encode('utf-8')
        cipher = AESCipher(key_bytes)

        # 2. Tạo IV (Initialization Vector) 16 byte ngẫu nhiên
        iv = os.urandom(BLOCK_SIZE)
        
        # 3. Khởi tạo giá trị ciphertext của khối trước đó (ban đầu là IV)
        previous_ciphertext_block = iv

        # 4. Mở file đọc (input) và file ghi (output)
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            # 5. GHI 16 byte IV vào ĐẦU file output
            f_out.write(iv)
            
            while True:
                # 6. Đọc từng khối 16 byte
                plaintext_block = f_in.read(BLOCK_SIZE)
                
                if len(plaintext_block) == 16:
                    # Đây là một khối đầy đủ, cứ mã hóa
                    block_to_encrypt = _xor_bytes(plaintext_block, previous_ciphertext_block)
                    ciphertext_block = cipher.encrypt_block(block_to_encrypt)
                    f_out.write(ciphertext_block)
                    previous_ciphertext_block = ciphertext_block
                
                else:
                    # Đây là khối cuối cùng (hoặc file rỗng)
                    # Nó có thể có 0 < byte < 16, hoặc 0 byte
                    
                    # 7. Áp dụng padding PKCS#7
                    # Nếu len=2, thêm 14 byte
                    # Nếu len=0, thêm 16 byte 
                    padded_block = pad_pkcs7(plaintext_block, BLOCK_SIZE)
                    
                    # 8. Mã hóa khối cuối cùng đã đệm
                    block_to_encrypt = _xor_bytes(padded_block, previous_ciphertext_block)
                    ciphertext_block = cipher.encrypt_block(block_to_encrypt)
                    f_out.write(ciphertext_block)
                    
                    # 9. Thoát khỏi vòng lặp
                    break 

    except ValueError as e:
        # Lỗi này xảy ra nếu key_string có độ dài sai
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
        # 1. Chuyển đổi khóa và khởi tạo AESCipher
        key_bytes = key_string.encode('utf-8')
        cipher = AESCipher(key_bytes)

        # 2. Mở file đọc (input) và file ghi (output)
        with open(input_filepath, 'rb') as f_in, open(output_filepath, 'wb') as f_out:
            
            # 3. ĐỌC 16 byte ĐẦU TIÊN để lấy IV 
            iv = f_in.read(BLOCK_SIZE)
            if len(iv) < BLOCK_SIZE:
                raise FileHandlerError("File quá nhỏ hoặc bị hỏng, không chứa IV.")
            
            # 4. Khởi tạo giá trị ciphertext của khối trước đó (ban đầu là IV)
            previous_ciphertext_block = iv 
            
            # 5. Sử dụng kỹ thuật "đọc trước" để xử lý khối cuối cùng
            # Đọc khối đầu tiên của dữ liệu
            current_ciphertext_block = f_in.read(BLOCK_SIZE) 
            
            while True:
                # Đọc khối tiếp theo
                next_ciphertext_block = f_in.read(BLOCK_SIZE)
                
                if not next_ciphertext_block:
                    # Nếu không còn khối 'next', thì khối 'current' là khối cuối
                    if not current_ciphertext_block:
                        # File rỗng (chỉ có IV), không làm gì cả
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
                        # Lỗi xảy ra khi dùng SAI KHÓA
                        raise FileHandlerError(f"Lỗi gỡ đệm. Rất có thể bạn đã nhập sai khóa. Chi tiết: {e}")
                    
                    # Ghi khối cuối đã gỡ đệm vào file 
                    f_out.write(unpadded_block)
                    
                    # Kết thúc vòng lặp
                    break
                
                # --- Nếu khối 'next' tồn tại (tức là 'current' KHÔNG phải khối cuối) ---
                
                if len(current_ciphertext_block) != BLOCK_SIZE:
                    raise FileHandlerError("File bị hỏng (khối dữ liệu không đủ 16 byte).")
                
                # 6. Giải mã khối 'current'
                decrypted_block = cipher.decrypt_block(current_ciphertext_block)
                
                # 7. Hiện thực logic CBC (Giải mã) 
                plaintext_block = _xor_bytes(decrypted_block, previous_ciphertext_block)
                
                # 8. Ghi khối đã giải mã vào file (KHÔNG gỡ đệm)
                f_out.write(plaintext_block)
                
                # 9. Cập nhật trạng thái cho vòng lặp sau
                previous_ciphertext_block = current_ciphertext_block
                current_ciphertext_block = next_ciphertext_block

    except ValueError as e:
        raise FileHandlerError(f"Lỗi khởi tạo AES: {e}")
    except FileNotFoundError:
        raise FileHandlerError(f"Lỗi: Không tìm thấy file đầu vào '{input_filepath}'")
    except Exception as e:
        # Đảm bảo bắt các lỗi tùy chỉnh 
        if not isinstance(e, FileHandlerError):
            raise FileHandlerError(f"Một lỗi đã xảy ra trong quá trình giải mã: {e}")
        else:
            raise e
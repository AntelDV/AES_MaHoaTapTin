
# Kích thước khối tiêu chuẩn của AES
BLOCK_SIZE = 16

class PaddingError(Exception):
    """
    Lỗi tùy chỉnh sẽ được ném ra nếu phát hiện đệm (padding) không hợp lệ.
    Điều này thường xảy ra khi giải mã bằng một khóa sai.
    """
    pass

def pad_pkcs7(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Thêm đệm PKCS#7 vào dữ liệu (dạng bytes).

    Nếu dữ liệu đã là bội số của block_size, một khối đệm 
    mới sẽ được thêm vào.
    
    Args:
        data: Dữ liệu đầu vào.
        block_size: Kích thước khối (mặc định là 16 cho AES).

    Returns:
        Dữ liệu đã được thêm đệm.
    """
    # Tính toán số byte cần thêm
    padding_len = block_size - (len(data) % block_size)
    
    # Tạo chuỗi byte đệm
    # Ví dụ: nếu padding_len = 5, padding = b'\x05\x05\x05\x05\x05'
    padding = bytes([padding_len]) * padding_len
    
    # Trả về dữ liệu gốc + đệm
    return data + padding

def unpad_pkcs7(data: bytes, block_size: int = BLOCK_SIZE) -> bytes:
    """
    Gỡ bỏ đệm PKCS#7 khỏi dữ liệu (dạng bytes).

    Hàm này sẽ kiểm tra tính hợp lệ của đệm trước khi gỡ bỏ.
    
    Args:
        data: Dữ liệu đã giải mã (có chứa đệm).
        block_size: Kích thước khối (mặc định là 16 cho AES).

    Returns:
        Dữ liệu gốc (đã gỡ bỏ đệm).
        
    Raises:
        PaddingError: Nếu đệm không hợp lệ.
    """
    if not data:
        raise PaddingError("Dữ liệu đầu vào rỗng, không thể gỡ đệm.")

    # Lấy giá trị của byte cuối cùng
    # Byte này cho biết có bao nhiêu byte đệm
    padding_len = data[-1]

    # Kiểm tra 1: Độ dài đệm phải hợp lệ
    # Không thể lớn hơn block_size và không thể bằng 0
    if padding_len > block_size or padding_len == 0:
        raise PaddingError("Giá trị byte đệm không hợp lệ.")

    # Kiểm tra 2: Tổng độ dài dữ liệu phải hợp lệ
    if len(data) < padding_len:
        raise PaddingError("Độ dài dữ liệu ngắn hơn độ dài đệm báo cáo.")

    # Kiểm tra 3: Tất cả các byte đệm phải có cùng giá trị
    # Lấy ra các byte đệm
    padding = data[-padding_len:]
    # Kiểm tra xem tất cả các byte trong đó có bằng padding_len không
    for byte in padding:
        if byte != padding_len:
            raise PaddingError("Nội dung các byte đệm không nhất quán.")

    # Nếu tất cả kiểm tra đều qua, gỡ bỏ đệm và trả về
    return data[:-padding_len]
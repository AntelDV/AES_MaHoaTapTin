# --- Các bảng và hằng số của AES  ---
S_BOX = [
    0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76,
    0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0,
    0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15,
    0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75,
    0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84,
    0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf,
    0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8,
    0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2,
    0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73,
    0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb,
    0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79,
    0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08,
    0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a,
    0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e,
    0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf,
    0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16
]

INV_S_BOX = [
    0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb,
    0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb,
    0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e,
    0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25,
    0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92,
    0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84,
    0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06,
    0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b,
    0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73,
    0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e,
    0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b,
    0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4,
    0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f,
    0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef,
    0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61,
    0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d
]

MIX_COLUMNS_MATRIX = [
    [0x02, 0x03, 0x01, 0x01],
    [0x01, 0x02, 0x03, 0x01],
    [0x01, 0x01, 0x02, 0x03],
    [0x03, 0x01, 0x01, 0x02]
]

INV_MIX_COLUMNS_MATRIX = [
    [0x0e, 0x0b, 0x0d, 0x09],
    [0x09, 0x0e, 0x0b, 0x0d],
    [0x0d, 0x09, 0x0e, 0x0b],
    [0x0b, 0x0d, 0x09, 0x0e]
]

# Hằng số RCON cho Key Expansion
RCON = [
    0x8d, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36
]


class AESCipher:
    """
    các độ dài khóa 128-bit (10 vòng), 192-bit (12 vòng), và 256-bit (14 vòng).
    """

    def __init__(self, key):
        """
        Khởi tạo bộ mã hóa AES với khóa (key) cung cấp.
        Khóa phải là 16, 24, hoặc 32 byte.
        """
        # 1. Kiểm tra độ dài khóa
        key_len = len(key)
        if key_len not in [16, 24, 32]:
            raise ValueError("Độ dài khóa không hợp lệ (phải là 16, 24, hoặc 32 byte).") 

        # 2. Thiết lập các tham số dựa trên độ dài khóa 
        self.key = key
        # Nk: Số "từ" 32-bit trong khóa (4, 6, hoặc 8)
        self.nk = key_len // 4
        # Nr: Số vòng lặp (10, 12, hoặc 14)
        if self.nk == 4:
            self.num_rounds = 10  # AES-128
        elif self.nk == 6:
            self.num_rounds = 12  # AES-192
        else:
            self.num_rounds = 14  # AES-256

        # Nb: Số cột (từ 32-bit) trong State (luôn là 4)
        self.nb = 4

        # 3. Sinh toàn bộ khóa vòng 
        self.round_keys = self._key_expansion() 

    def _sub_word(self, word):
        """
        Áp dụng S-box cho mỗi byte trong một "từ" (word) 4 byte.
        Đây là một phần của Key Expansion.
        """
        return [S_BOX[b] for b in word]

    def _rot_word(self, word):
        """
        Dịch vòng trái 1 byte cho một "từ" (word).
        [b0, b1, b2, b3] -> [b1, b2, b3, b0]
        """
        return word[1:] + word[:1]

    def _key_expansion(self):
        """
        Mở rộng khóa chính thành danh sách các khóa vòng.
        Hàm này đã được sửa đổi từ Bài 6 để hỗ trợ Nk = 4, 6, 8.
        """
        # Chuyển khóa chính thành danh sách các "từ" (mỗi từ 4 byte)
        key_words = list(self._to_words(self.key)) 
        
        # Số lượng "từ" cần sinh = Nb * (Nr + 1)
        # AES-128 (Nr=10) cần 4 * (10+1) = 44 "từ"
        # AES-256 (Nr=14) cần 4 * (14+1) = 60 "từ"
        num_words_needed = self.nb * (self.num_rounds + 1)
        
        i = self.nk
        while i < num_words_needed:
            temp = list(key_words[i - 1])  # Lấy "từ" trước đó 

            # Áp dụng hàm g() nếu i là bội số của Nk
            if i % self.nk == 0:
                temp = self._rot_word(temp)  # RotWord 
                temp = self._sub_word(temp)  # SubWord 
                temp[0] = temp[0] ^ RCON[i // self.nk]  # XOR với RCON 
            
            # Trường hợp đặc biệt cho AES-256 (Nk=8)
            # Nếu i % Nk == 4, chỉ cần SubWord
            elif self.nk == 8 and i % self.nk == 4:
                temp = self._sub_word(temp)

            # XOR với "từ" thứ (i - Nk) để tạo "từ" mới
            xor_word = key_words[i - self.nk] 
            new_word = [xor_word[j] ^ temp[j] for j in range(4)]
            
            key_words.append(new_word)
            i += 1

        # Chia danh sách các "từ" thành các "khóa vòng" (dạng ma trận 4x4)
        round_keys = []
        for i in range(self.num_rounds + 1):
            round_key = [[0, 0, 0, 0] for _ in range(4)] 
            # Sắp xếp lại theo cột-hàng để tối ưu hàm AddRoundKey
            for col in range(4): 
                for row in range(4): 
                    round_key[col][row] = key_words[i * self.nb + col][row]
            round_keys.append(round_key) 

        return round_keys 




    # --- Các hàm chuyển đổi  ---
    
    def _to_words(self, key):
        """Chuyển khóa (bytes) thành các "từ" 4 byte"""
        words = []
        for i in range(0, len(key), 4): 
            words.append(list(key[i:i+4])) 
        return words 

    def _to_state(self, block):
        """Chuyển khối 16 byte (bytes) thành ma trận State 4x4."""
        state = [[0, 0, 0, 0] for _ in range(4)]
        for r in range(4): 
            for c in range(4): 
                # Sắp xếp theo cột-chính (column-major)
                state[r][c] = block[c * 4 + r] 
        return state 

    def _from_state(self, state):
        """Chuyển ma trận State 4x4 về khối 16 byte (bytes)."""
        block = bytearray(16)
        for r in range(4): 
            for c in range(4): 
                block[c * 4 + r] = state[r][c] 
        return bytes(block) 




    # --- Các hàm của vòng lặp AES  ---
    
    def _sub_bytes(self, state, sbox):
        """Thay thế từng byte trong State bằng S-box."""
        for r in range(4): 
            for c in range(4): 
                state[r][c] = sbox[state[r][c]] 

    def _shift_rows(self, state):
        """Dịch vòng trái các hàng của State."""
        # Hàng 0: không dịch 
        # Hàng 1: Dịch trái 1 
        state[1] = state[1][1:] + state[1][:1] 
        # Hàng 2: Dịch trái 2 
        state[2] = state[2][2:] + state[2][:2] 
        # Hàng 3: Dịch trái 3 
        state[3] = state[3][3:] + state[3][:3] 

    def _inv_shift_rows(self, state):
        """Dịch vòng phải (nghịch đảo) các hàng của State."""
        # Hàng 1: Dịch phải 1 
        state[1] = state[1][-1:] + state[1][:-1] 
        # Hàng 2: Dịch phải 2 
        state[2] = state[2][-2:] + state[2][:-2] 
        # Hàng 3: Dịch phải 3 
        state[3] = state[3][-3:] + state[3][:-3] 

    def _mix_columns(self, state, matrix):
        """Nhân ma trận (trộn cột) trên trường GF(2^8)."""
        new_state = [[0, 0, 0, 0] for _ in range(4)]
        for c in range(4): 
            for r in range(4): 
                val = 0 
                for i in range(4): 
                    # Phép nhân Galois 
                    val ^= self._gf_mult(matrix[r][i], state[i][c]) 
                new_state[r][c] = val 
        state[:] = new_state 

    def _gf_mult(self, a, b):
        """Phép nhân trên trường Galois GF(2^8)."""
        p = 0 
        hi_bit_set = 0 
        for _ in range(8): 
            if (b & 1) == 1:
                p ^= a 
            
            hi_bit_set = a & 0x80 
            a <<= 1 
            if hi_bit_set == 0x80: 
                a ^= 0x1b  # Đa thức x^8 + x^4 + x^3 + x + 1 (0x11b) 
            
            b >>= 1 
        return p % 256 

    def _add_round_key(self, state, round_key):
        """XOR State với Khóa vòng."""
        for r in range(4): 
            for c in range(4): 
                state[r][c] ^= round_key[c][r]




    # --- Các hàm Mã hóa / Giải mã chính ---

    def encrypt_block(self, plaintext):
        """
        Mã hóa một khối 16 byte (plaintext).
        """
        if len(plaintext) != 16:
            raise ValueError("Khối bản rõ phải có đúng 16 byte.") 
        
        state = self._to_state(plaintext) 

        # Vòng đầu tiên 
        self._add_round_key(state, self.round_keys[0]) 

        # Các vòng lặp chính (Nr - 1 vòng) 
        for i in range(1, self.num_rounds): 
            self._sub_bytes(state, S_BOX) 
            self._shift_rows(state) 
            self._mix_columns(state, MIX_COLUMNS_MATRIX) 
            self._add_round_key(state, self.round_keys[i])

        # Vòng cuối cùng (Không có MixColumns) 
        self._sub_bytes(state, S_BOX) 
        self._shift_rows(state) 
        self._add_round_key(state, self.round_keys[self.num_rounds]) 

        return self._from_state(state) 

    def decrypt_block(self, ciphertext):
        """
        Giải mã một khối 16 byte (ciphertext).
        """
        if len(ciphertext) != 16:
            raise ValueError("Khối bản mã phải có đúng 16 byte.") 
        
        state = self._to_state(ciphertext) 

        # Vòng đầu tiên (ngược) 
        self._add_round_key(state, self.round_keys[self.num_rounds]) 
        self._inv_shift_rows(state) 
        self._sub_bytes(state, INV_S_BOX) 

        # Các vòng lặp chính (ngược) 
        for i in range(self.num_rounds - 1, 0, -1):
            self._add_round_key(state, self.round_keys[i]) 
            self._mix_columns(state, INV_MIX_COLUMNS_MATRIX) 
            self._inv_shift_rows(state) 
            self._sub_bytes(state, INV_S_BOX) 

        # Vòng cuối cùng (ngược) 
        self._add_round_key(state, self.round_keys[0]) 

        return self._from_state(state)
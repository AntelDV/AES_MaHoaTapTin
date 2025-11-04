import customtkinter as ctk
from gui.app import Application

ctk.set_appearance_mode("dark")  
ctk.set_default_color_theme("blue") 

def main():
    try:
        app = Application()
        app.mainloop()
        
    except ImportError as e:
        print("="*50)
        print(f"\nChi tiết lỗi: {e}")
        print("="*50)
    except Exception as e:
        print(f"Một lỗi không mong muốn đã xảy ra: {e}")

if __name__ == "__main__":
    main()
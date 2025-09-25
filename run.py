from modules.ui import BinImgOpsApp

def main():
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except Exception:
        pass

    app = BinImgOpsApp()
    app.mainloop()

if __name__ == "__main__":
    main()
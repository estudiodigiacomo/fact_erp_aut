from gui_main import main_gui

def main():
    try:
        main_gui()
        pass
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
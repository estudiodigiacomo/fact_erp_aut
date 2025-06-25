from gui_main import run_automated_process

def main():
    try:
        run_automated_process()
    except Exception as e:
        print(f"An error occurred: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()

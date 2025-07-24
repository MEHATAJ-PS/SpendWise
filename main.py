from auth import AuthWindow

if __name__ == "__main__":
    try:
        app = AuthWindow()
        app.mainloop()
    except Exception as e:
        print("An error occurred:", e)

from app import app

if __name__ == '__main__':

    # run the app, this MUST be wrapped in main thread
    app.run(debug=True, port=5001)
from app import app

if __name__ == '__main__':

    # run the app, this MUST be wrapped in main thread, we will be running the dev server on port 5000
    app.run(debug=True, port=5001)
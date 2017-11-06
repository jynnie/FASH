from fash import app
from fash.constants import PORT, DEBUG
import os

# Run the application
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(
        host='0.0.0.0',
        port=PORT,
        debug=DEBUG
    )

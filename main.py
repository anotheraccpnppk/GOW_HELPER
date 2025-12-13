import certifi
import os
os.environ['SSL_CERT_FILE'] = certifi.where()
from app.windows.main_window import ProfileFetcherApp
if __name__ == "__main__":
    app = ProfileFetcherApp()
    app.mainloop()
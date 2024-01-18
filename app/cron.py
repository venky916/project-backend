# your_app/management/commands/keep_endpoints_alive.py
from datetime import datetime
import requests
import logging
logger = logging.getLogger( __name__ )

def handle(self, *args, **options):
    # Replace these URLs with your actual frontend and backend URLs
    frontend_url = 'https://next-app-h2qh.onrender.com'
    backend_url = "https://backend-app-ygah.onrender.com/api/"
    
    print(f'Task executed at {datetime.now()}')
    # Make requests to keep endpoints alive
    response_frontend = requests.get(frontend_url)
    logger.info(response_frontend)
    response_backend = requests.get(backend_url)
    logger.info(response_backend)
    print(response_backend,response_frontend)

    self.stdout.write(self.style.SUCCESS(f'Frontend status code: {response_frontend.status_code}'))
    self.stdout.write(self.style.SUCCESS(f'Backend status code: {response_backend.status_code}'))

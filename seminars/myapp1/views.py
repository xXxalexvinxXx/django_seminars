import logging
from django.shortcuts import render

logger = logging.getLogger('page_visits')

def index(request):
    logger.info('Index page accessed')
    return render(request, 'myapp1/index.html')

def about(request):
    logger.info('About page accessed')
    return render(request, 'myapp1/about.html')
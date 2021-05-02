from os import listdir
from os.path import join, isdir, isfile

from django.conf.urls import include, url

from backend.settings import BASE_DIR

entities = [directory
            for directory in listdir(join(BASE_DIR, 'api'))
            if (isdir(join(BASE_DIR, 'api', directory))
                and isfile(join(BASE_DIR, 'api', directory, 'urls.py')))
                and directory != '__pycache__'
            ]

urlpatterns = [
    url(r'', include(f'api.{entity}.urls'))  for entity in entities
]
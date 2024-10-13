# Showcasing "hot spots"
# where certain locations are queried more frequently than others
# increasing the likelihood of cache hits.

from locust import HttpUser, TaskSet, task
import random

class UserBehavior(TaskSet):
    locations = ['Aaronfort', 'Abigailton', 'Abigailtown', 'Acevedofourt', 'Abigailshire']

    # weighted list to favor certain locations (e.g., 'Aaronfort' and 'Abigailton')
    weighted_locations = ['Aaronfort'] * 50 + ['Abigailton'] * 30 + ['Abigailtown'] * 10 + ['Acevedofourt'] * 5 + ['Abigailshire'] * 5

    @task
    def query_weather(self):
        # POST query to server with a location picked from a weighted distribution
        location = random.choice(self.weighted_locations)
        self.client.post('/query', data={'location': location})

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    min_wait = 1000 # wait between tasks in milliseconds
    max_wait = 2000

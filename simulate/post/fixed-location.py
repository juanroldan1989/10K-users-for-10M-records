# In a real-world scenario, users might query the same location repeatedly
# e.g., a user checking weather for their hometown
# We assign each virtual user a specific location and
# have them always query the same one throughout their session.

from locust import HttpUser, TaskSet, task
import random

class UserBehavior(TaskSet):
  def on_start(self):
    # Assign a specific location to each user upon starting
    self.location = random.choice(['Aaronfort', 'Abigailton', 'Abigailtown', 'Acevedofourt', 'Abigailshire'])

  @task
  def query_weather(self):
    # POST query to server using the fixed location for this user
    self.client.post('/query', data={'location': self.location})

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  min_wait = 1000 # wait between tasks in milliseconds
  max_wait = 2000

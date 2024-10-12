from locust import HttpUser, TaskSet, task
import random

class UserBehavior(TaskSet):
  @task
  def query_weather(self):
    locations = ['Aaronburgh', 'Aaronbury', 'Aaronmouth', 'Aaronstad', 'Aaronton']
    self.client.post('/query', data={'location': random.choice(locations)})

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  min_wait = 1000 # wait between tasks in milliseconds
  max_wait = 2000

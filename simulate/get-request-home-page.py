from locust import HttpUser, TaskSet, task

class UserBehavior(TaskSet):
  @task
  def query_weather(self):
    # GET homepage
    self.client.get('/')

class WebsiteUser(HttpUser):
  tasks = [UserBehavior]
  min_wait = 1000 # wait between tasks in milliseconds
  max_wait = 2000

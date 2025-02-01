from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.tasks.models import Task


class TasksListViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Test Label')
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(name='Active',description="test",status=self.status,performer=self.user,creator=self.user)
        self.task.labels.set([self.label])
        self.url = reverse('tasks')

    def test_tasks_list_authenticated(self):
        # Логинимся и проверяем, что страница статусов доступна
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')


class TaskCreateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Test Label')
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(name='Test Task',description="test",status=self.status,performer=self.user,creator=self.user)
        self.task.labels.set([self.label])
        self.url = reverse('tasks_create')

    def test_create_task_authenticated(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'New Task',"description": "test", "status": self.status.id, "performer": self.user.id,"labels": [self.label.id]})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('tasks'))
        self.assertTrue(Task.objects.filter(name='New Task').exists())


class TaskUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Test Label')
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(name='Old Task',description="test",status=self.status,performer=self.user,creator=self.user)
        self.task.labels.set([self.label])
        self.url = reverse('tasks_update', args=[self.task.id])

    def test_update_task_authenticated(self):
        # Логинимся и обновляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'Updated Task',"description": "test", "status": self.status.id, "performer": self.user.id,"labels": [self.label.id]})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('tasks'))
        self.task.refresh_from_db()
        self.assertEqual(self.task.name, 'Updated Task')


class TaskDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Test Label')
        self.status = Status.objects.create(name='Test Status')
        self.task = Task.objects.create(name='Task to be deleted', description="test",status=self.status,performer=self.user,creator=self.user)
        self.task.labels.set([self.label])
        self.url = reverse('tasks_delete', args=[self.task.id])

    def test_delete_task_authenticated(self):
        # Логинимся и удаляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('tasks'))
        self.assertFalse(Task.objects.filter(name='Task to be deleted').exists())

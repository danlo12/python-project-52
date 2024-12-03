from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from task_manager.models import CustomUser, Label, Status, Task


class UserRegistrationTest(TestCase):
    def test_register_user(self):
        response = self.client.post(reverse('user-create'),{
            'first_name':'John',
            'last_name':'Smith',
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'TestPassword',
            'password_check':'TestPassword',
        })

        self.assertEqual(response.status_code, 302)

        self.assertTrue(CustomUser.objects.filter(username='newuser').exists())


class UserAuthTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password
        )
    def test_login_user(self):
        response = self.client.post(reverse('login'),{
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_logout_user(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

class UserUpdateTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPassword123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name='OldFirstName',
            last_name='OldLastName'
        )
        self.client.login(username=self.username, password=self.password)

    def test_update_user(self):
        response = self.client.post(reverse('update',args=[self.user.id]), {
            'first_name': 'NewFirstName',
            'last_name': 'NewLastName',
            'username': self.username,
            'password': self.password,
            'password_check': self.password
        })
        self.assertEqual(response.status_code, 302)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'NewFirstName')
        self.assertEqual(self.user.last_name, 'NewLastName')

class UserDeleteTest(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'TestPassword123'
        self.user = get_user_model().objects.create_user(
            username=self.username,
            password=self.password,
            first_name='OldFirstName',
            last_name='OldLastName'
        )
        self.client.login(username=self.username, password=self.password)

    def test_delete_user(self):
        response = self.client.post(reverse('delete_user',args=[self.user.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(get_user_model().objects.filter(id=self.user.id).exists())


class StatusesListViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Active')
        self.url = reverse('statuses')  # предполагается, что url для списка статусов называется 'statuses'

    def test_statuses_list_authenticated(self):
        # Логинимся и проверяем, что страница статусов доступна
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')

class StatusesCreateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('status_create')  # предполагается, что url для создания статуса называется 'status_create'

    def test_create_status_authenticated(self):
        # Логинимся и создаем новый статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'New Status'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('statuses'))  # После создания редирект на страницу статусов
        self.assertTrue(Status.objects.filter(name='New Status').exists())


class StatusesUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Old Status')
        self.url = reverse('status_update', args=[self.status.id])

    def test_update_status_authenticated(self):
        # Логинимся и обновляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'Updated Status'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('statuses'))
        self.status.refresh_from_db()
        self.assertEqual(self.status.name, 'Updated Status')



class StatusesDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.status = Status.objects.create(name='Status to be deleted')
        self.url = reverse('status_delete', args=[self.status.id])

    def test_delete_status_authenticated(self):
        # Логинимся и удаляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('statuses'))
        self.assertFalse(Status.objects.filter(name='Status to be deleted').exists())

class LabelsListViewTest(TestCase):

    def setUp(self):
        # Создаем пользователя
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Active')
        self.url = reverse('labels')

    def test_labels_list_authenticated(self):
        # Логинимся и проверяем, что страница статусов доступна
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Active')

class LabelsCreateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.url = reverse('label_create')

    def test_create_label_authenticated(self):
        # Логинимся и создаем новый статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'New Label'})
        self.assertEqual(response.status_code, 302)  # Статус 302, т.к. будет редирект на страницу списка
        self.assertRedirects(response, reverse('labels'))
        self.assertTrue(Label.objects.filter(name='New Label').exists())

class LabelUpdateViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Old Label')
        self.url = reverse('label_update', args=[self.label.id])

    def test_update_label_authenticated(self):
        # Логинимся и обновляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url, {'name': 'Updated Label'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.label.refresh_from_db()
        self.assertEqual(self.label.name, 'Updated Label')

class LabelDeleteViewTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpassword')
        self.label = Label.objects.create(name='Label to be deleted')
        self.url = reverse('label_delete', args=[self.label.id])

    def test_delete_label_authenticated(self):
        # Логинимся и удаляем статус
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('labels'))
        self.assertFalse(Status.objects.filter(name='Label to be deleted').exists())


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

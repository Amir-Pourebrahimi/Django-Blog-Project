from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse

from .models import Post


class BlogPostTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create(username='user1')
        cls.post1 = Post.objects.create(
            title='post1',
            text='hello every body',
            status=Post.STATUS_CHOICES[0][0],  # published
            author=cls.user,
        )
        cls.post2 = Post.objects.create(
            title='post2',
            text='draftpost',
            status=Post.STATUS_CHOICES[1][0],  # draft
            author=cls.user,
        )

    def test_post_model_str(self):
        post = self.post1
        self.assertEqual(str(post), post.title)

    def test_post_detail(self):
        self.assertEqual(self.post1.title, 'post1')
        self.assertEqual(self.post1.text, 'hello every body')

    def test_post_list_url(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_post_list_url_by_name(self):
        response = self.client.get(reverse('posts_list'))
        self.assertEqual(response.status_code, 200)

    def test_detail_page_url(self):
        response = self.client.get(f'/blog/{self.post1.id}/')
        self.assertEqual(response.status_code, 200)

    def test_detail_page_url_by_name(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertEqual(response.status_code, 200)

    def test_title_on_blog_lists_page(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)

    def test_details_on_blog_details_page(self):
        response = self.client.get(reverse('post_detail', args=[self.post1.id]))
        self.assertContains(response, self.post1.title)
        self.assertContains(response, self.post1.text)

    def test_status_code_404_if_page_id_not_exist(self):
        response = self.client.get(reverse('post_detail', args=[999]))
        self.assertEqual(response.status_code, 404)

    def test_draft_post_not_show(self):
        response = self.client.get(reverse('posts_list'))
        self.assertContains(response, self.post1.title)
        self.assertNotContains(response, self.post2.title)

    def test_post_create_view(self):
        response = self.client.post(reverse('post_create'), {
            'title': 'post method',
            'text': 'test post method',
            'status': 'pub',
            'author': self.user.id,
        })

        self.assertEqual(response.status_code, 302),
        self.assertEqual(Post.objects.last().title, 'post method')
        self.assertEqual(Post.objects.last().text, 'test post method')

    def test_post_update_view(self):
        response = self.client.post(reverse('post_update', args=[self.post2.id]), {
            'title': 'post2 Updated',
            'text': 'test post2 Updated',
            'status': 'pub',
            'author': self.post2.author.id,
        })

        self.assertEqual(response.status_code, 302),
        self.assertEqual(Post.objects.last().title, 'post2 Updated')
        self.assertEqual(Post.objects.last().text, 'test post2 Updated')

    def test_post_delete_view(self):
        response = self.client.post(reverse('post_delete', args=[self.post2.id]))
        self.assertEqual(response.status_code, 302)

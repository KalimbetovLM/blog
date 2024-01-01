from django.test import TestCase
from django.urls import reverse
from posts.models import Post,Comment
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from django.utils import timezone
from datetime import timedelta

# class PostsTestCase(TestCase):

#     def test_no_posts_found(self):
#         response = self.client.get(reverse("posts:post_list"))

#         self.assertContains(response,"No posts found")

#     def test_posts_list(self):
#         user = User.objects.create(username="Userbek")
#         user.set_password("password12345")
#         user.save()

#         self.client.login(username="Userbek",password="password12345")

#         post1 = Post.objects.create(author=user,title="Birinchi test title",text="Birinchi test text",status=Post.Status.Verified)
#         post2 = Post.objects.create(author=user,title="Ikkinchi test title",text="Ikkinchi test text",status=Post.Status.Verified)
#         post3 = Post.objects.create(author=user,title="Uchinchi test title",text="Uchinchi test text",status=Post.Status.Verified)        

#         response = self.client.get(reverse("posts:post_list") + "?page=1" )

#         for post in [post1,post2]:
#             self.assertContains(response,post.title)
#             self.assertContains(response,post.text)
        
#         response = self.client.get(reverse("posts:post_list") + "?page=2")

#         self.assertContains(response,post3.title)
#         self.assertContains(response,post3.text)
    
#     def test_post_details(self):
#         user = User.objects.create(username="Userbek")
#         user.set_password("password12345")
#         user.save()
        
#         self.client.login(username="Userbek",password="password12345")

#         post = Post.objects.create(title="Test title",text="Test text",author=user,status=Post.Status.Verified)

#         response = self.client.get(reverse("posts:post_detail", kwargs={"pk":post.pk}))

#         self.assertContains(response,post.title)
#         self.assertContains(response,post.text)

#     def test_weeks_popular_posts(self):
#         user = User.objects.create(username="user")
#         user.set_password("password12345")
#         user.save()
#         self.client.login(username="user",password="password12345")

#         post = Post.objects.create(author=user,title="First test title",text="First test text",status=Post.Status.Verified)
#         start_time = (timezone.now() - timedelta(days=7))

#         response = self.client.get(reverse("posts:weekend"))

#         self.assertContains(response,post.title)
#         self.assertContains(response,post.text)
#         self.assertTrue(start_time < post.publish_time)

#     def test_months_popular_posts(self):
#         user = User.objects.create(username="user")
#         user.set_password("password12345")
#         user.save()
#         self.client.login(username="user",password="password12345")

#         post = Post.objects.create(author=user,title="Test title",text="Test text",status=Post.Status.Verified)
#         start_time = (timezone.now() - timedelta(days=30))

#         response = self.client.get(reverse("posts:month"))

#         self.assertContains(response,post.title)
#         self.assertContains(response,post.text)
#         self.assertTrue(start_time < post.publish_time)

#     def test_recommended_posts(self):
#         user = User.objects.create(username="user")
#         user.set_password("password12345")
#         user.save()
#         self.client.login(username="user",password="password12345")

#         recommended_post = Post.objects.create(author=user,title="Test title 1",text="Test text 1",status=Post.Status.Verified,
#                                    recommendation=Post.Recommendation.Recommended)
#         not_recommended_post = Post.objects.create(author=user,title="Test title 2",text="Test text 2",status=Post.Status.Verified,
#                                    recommendation=Post.Recommendation.NotRecommended)
        
#         response = self.client.get(reverse("posts:recommended"))
#         posts_count = Post.objects.count()

#         self.assertEqual(posts_count,2)
#         self.assertContains(response,recommended_post.title)
#         self.assertContains(response,recommended_post.text)
#         self.assertNotContains(response,not_recommended_post.title)
#         self.assertNotContains(response,not_recommended_post.text)

#     def test_popular_posts(self):
#         # User yaratamiz
#         user = User.objects.create(username="user1")
#         user.set_password("password123")
#         user.save()
#         self.client.login(username="user1",password="password123")

#         # Postlar yaratamiz
#         post1 = Post.objects.create(author=user,title="Birinchi test title",text="Birinchi test text",status=Post.Status.Verified)            
#         post2 = Post.objects.create(author=user,title="Ikkinchi test title",text="Ikkinchi test text",status=Post.Status.Verified)                                    
#         post3 = Post.objects.create(author=user,title="Uchinchi test title",text="Uchinchi test text",status=Post.Status.Verified)                                    
    
#         # Yaratilgan userlar yordamida kerali postlarning detail'iga request jo'natamiz(chunki,faqat shundagina hitcount ishga tushadi)
#         self.client.get(reverse("posts:post_detail",kwargs={"pk":post3.pk}))
#         self.client.get(reverse("posts:post_detail",kwargs={"pk":post2.pk}))
        
#         response = self.client.get(reverse("posts:popular"))

#         # Shu usul bilan post3 va post2 ning viewlar soni ko'p bo'lgani uchun birinchi page'da,post1'ning esa viewlar soni eng
#         # kam bo'lgani uchun ikkinchi page'da kelayotganini tekshiramiz.Agar testlar OK qaytarsa demak postlar viewlar miqdori bo'yicha 
#         # tartiblangan bo'ladi

#         self.assertContains(response,post3.title)
#         self.assertContains(response,post3.text)
#         self.assertEqual(post3.hit_count_generic.count(),1)
#         self.assertContains(response,post2.title)
#         self.assertContains(response,post2.text)
#         self.assertEqual(post2.hit_count_generic.count(),1)
#         self.assertNotContains(response,post1.title)
#         self.assertNotContains(response,post1.text)

#     def test_created_post(self):
#         user = User.objects.create(username="user1")
#         user.set_password("password123")
#         user.save()
#         self.client.login(username="user1",password="password123")


#         self.client.post(reverse("posts:post_create"),
#                                    data = {
#                                        "title":"Test title",
#                                        "text":"Test text"
#                                    })
#         posts_count = Post.objects.count()
#         self.assertEqual(posts_count,1)

class CommentsTestCase(TestCase):
    
    def test_created_comment_displays(self):

        user = User.objects.create(username="user1")
        user.set_password("password123")
        user.save()
        self.client.login(username="user1",password="password123")


        post = Post.objects.create(
            title="Test title",
            text = "Test text",
            author=user,
            status = Post.Status.Verified
        )

        comment = Comment.objects.create(
            post = post,
            author = user,
            text = "Test comment"
        )
        comments_count = Comment.objects.count()
        
        response = self.client.get(reverse("posts:post_detail",kwargs={"pk":post.pk}))
        
        self.assertEqual(comments_count,1)
        self.assertContains(response,comment.text)
        
    def test_create_comment(self):

        user = User.objects.create(username="user1")
        user.set_password("password123")
        user.save()
        self.client.login(username="user1",password="password123")
        
        post = Post.objects.create(
            title="Test title",
            text = "Test text",
            author=user,
            status = Post.Status.Verified
        )
        self.client.post(reverse("posts:post_detail",kwargs={"pk":post.pk}),
                         data={
                             "text":"Test comment"
                         })
        comment = Comment.objects.get(text="Test comment")
        comments_count = Comment.objects.count()
        response = self.client.get(reverse("posts:post_detail",kwargs={"pk":post.pk}))
        user1 = get_user(self.client)

        self.assertEqual(comments_count,1)
        self.assertContains(response,comment.text)
        self.assertEqual(comment.text,"Test comment")
        self.assertEqual(comment.author,user1)
        self.assertEqual(comment.post,post)
        
        
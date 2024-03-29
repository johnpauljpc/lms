from django.db import models
# from PIL import Image
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
class Categories(models.Model):
    icon = models.CharField(max_length=200,null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    
    def get_all_categories(self):
        return Categories.objects.all().order_by('id')



class Level(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Language(models.Model):
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name


class Author(models.Model):
    author_profile = models.ImageField(upload_to="Images/authors")
    name = models.CharField(max_length=100, null=True)
    specialty = models.CharField(max_length=100, default='web dev')
    about_author = models.TextField()

    def __str__(self):
        return self.name


class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Images/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    language = models.ForeignKey(Language, on_delete=models.CASCADE, null=True)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=True)
    deadline = models.CharField(null=True, max_length=100)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    certificate = models.BooleanField(null=True, default=False)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('course-detail', kwargs={'slug':self.slug})
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s" % (slug, qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class things_you_wil_learn(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.points
    class Meta:
        verbose_name_plural = "things you wil learn"
    

class Course_Requirements(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    points = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.points
    
    class Meta:
        verbose_name_plural = "Course Requirement"



class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.name} - {self.course.title}'
    

class Video(models.Model):
    serial_number = models.IntegerField(null=True, blank=True)
    thumbnail = models.ImageField( upload_to='Images/Video_imgs', null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=100)
    duration = models.IntegerField(null=True, blank=True)
    preview = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.title
    



class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    paid = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add= True)



    def __str__(self):
        return f'{self.user.first_name} - {self.course.title}'
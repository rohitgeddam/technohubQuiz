from django.db import models
from django.contrib.auth import get_user_model
from slugify import slugify
from django.urls import reverse
from django.utils import timezone
from ckeditor.fields import RichTextField
# Create your models here.
class Quiz(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255)
    description = RichTextField()
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, blank=True, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    # allowed_time = models.DurationField()
    roll_out = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'quizes'
    def __str__(self):
        return self.name
    

    def get_absolute_url(self):
        return reverse('quiz_start', args=(self.slug,))
        

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name='questions', on_delete=models.CASCADE)
    
    text = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now = True)

    

    def __str__(self):
        return self.text[:30]
    
class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options',  on_delete=models.CASCADE)
    text = RichTextField()
    is_answer = models.BooleanField(default=False)

    def __str__(self):
        return self.text[:30]
    
class QuizTaker(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='quiz_takers',  on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='quiz_takers',  on_delete=models.CASCADE)
    score = models.DecimalField(decimal_places=2, default=0.0, max_digits=4)

    def __str__(self):
        return self.user.username
    
    
class Response(models.Model):
    user = models.ForeignKey(get_user_model(), related_name='responses',  on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, related_name='responses', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='responses', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='responses',  on_delete=models.CASCADE, null=True, blank=True)
    
    correct_option = models.ForeignKey(Option, related_name='correct_response', on_delete=models.CASCADE)
    is_correct = models.BooleanField(default=False)
    def __str__(self):
        return f'{self.user.username}_{self.quiz.name}'
    
    
from django.contrib import admin
import nested_admin
from django.core.exceptions import ValidationError
from .models import Question, Quiz, Option, QuizTaker, Response
# Register your models here.


class OptionAdmin(nested_admin.NestedTabularInline):
    model = Option
    extra = 0
    

class QuestionAdmin(nested_admin.NestedStackedInline):
    model = Question
    inlines = [OptionAdmin]
    extra = 0
   
class QuizAdmin(nested_admin.NestedModelAdmin):
    list_display = ['name', 'start_time', 'end_time', 'roll_out']
    prepopulated_fields = {"slug": ('name',),}
    exclude = ['created_by',]
    inlines = [QuestionAdmin]

    def response_add(self, request, new_object):
        obj = self.after_saving_model_and_related_inlines(new_object)
        return super(QuizAdmin, self).response_add(request, obj)

    def response_change(self, request, obj):
        obj = self.after_saving_model_and_related_inlines(obj)
        return super(QuizAdmin, self).response_change(request, obj)

    def after_saving_model_and_related_inlines(self, obj):        
        all_questions = obj.questions.all()
        
       
        for q in all_questions:
            if(q.options.all().count() <= 0):
                raise ValidationError("Question cant be without options!")
            if (q.options.filter(is_answer=True).count() != 1):
                raise ValidationError("There can be/should be only one correct answer per question.")

        if(all_questions.count() <= 0):
            raise ValidationError("This quiz dosent have any questions")
        
        
        return obj
    
        # now we have what we need here... :)
        


    def save_model(self, request, obj, form, change):
        obj.created_by = request.user
        super(QuizAdmin, self).save_model(request, obj, form, change)


admin.site.register(Quiz, QuizAdmin)
admin.site.register(Response)
admin.site.register(QuizTaker)


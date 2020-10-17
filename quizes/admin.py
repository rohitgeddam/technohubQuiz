from django.contrib import admin
import nested_admin
from django.core.exceptions import ValidationError
from .models import Question, Quiz, Option, QuizTaker, Response

import decimal, csv
from django.http import HttpResponse

# Register your models here.


# export quiz result to csv action
def export_quiz_result_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="quiz_result.csv"'
    writer = csv.writer(response)
    question_weight = 1
    for query in queryset:
        writer.writerow([f'QUIZ NAME', 'TOTAL PARTICIPANTS', 'MAX SCORE ATTAINABLE'])
        total_number_of_questions = query.questions.all().count()
        quiz_takers_count = query.quiz_takers.all().count()
        writer.writerow([ query.name,quiz_takers_count, (total_number_of_questions * question_weight)])
        writer.writerow([" "])
        writer.writerow(['USERNAME', 'EMAIL', 'SCORE'])
        quiz_takers = query.quiz_takers.all().order_by('-score')

        for student in quiz_takers:
            writer.writerow([student.user.username, student.user.email, student.score])
    
        writer.writerow([" "])
    return response




export_quiz_result_to_csv.short_description = "Export Result To CSV"



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
    actions = [export_quiz_result_to_csv]

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


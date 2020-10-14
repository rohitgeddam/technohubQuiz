from django.shortcuts import render, redirect
from django.views.generic import ListView
from quizes.models import Quiz, QuizTaker, Response, Option
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model

from .decorators import profile_completion_required, quiz_started
from django.utils import timezone

from django.db.models import Count, Sum, Q

import time
# Create your views here.


GLOBAL_LEADERBOARD_SCORE= 'gleaderboard.scores'
GLOBAL_LEADERBOARD_PARTICIPANTS= 'gleaderboard.participants'


def HomePageView(request):
    on_going_quiz = Quiz.objects.filter(Q(roll_out=True) & Q(start_time__lte=timezone.now()) & Q(end_time__gte=timezone.now())).order_by('-start_time')
    
    up_comming_quiz = Quiz.objects.filter(Q(roll_out=True) & Q(start_time__gte=timezone.now())).order_by('start_time')
    past_quiz = Quiz.objects.filter(Q(roll_out=True) & Q(end_time__lte=timezone.now())).order_by('-end_time')
    
    context = {
        "on_going_quiz": on_going_quiz,
        "upcomming_quiz": up_comming_quiz,
        "past_quiz": past_quiz,
    }
    return render(request, "home.html", context)

@login_required
@profile_completion_required()
@quiz_started()
def QuizStartPage(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()
    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0
    user = request.user
    remaining_time_sec = int((quiz.end_time - timezone.now()).total_seconds())
    print("attem[ted", attempted); 
    if(attempted):
        score = QuizTaker.objects.filter(user=user, quiz=quiz).first().score
        
        user_response = []
        score = 0
        total_questions = len(questions)

        for question in questions:
          
            # try:
            response = Response.objects.filter(user=user,quiz=quiz,question=question).first()
            data = {
                "question":question,
                "is_correct": response.is_correct,
                "user_option": response.option,
                "correct_option": response.correct_option
            }
            # except:

            #     data = {
            #         "is_correct": False,
            #         "user_option": None,
            #         "correct_option": response.correct_option
            #     }
            if (response.is_correct):
                score = score + 1

            user_response.append(data)

        percentage = (score/total_questions) * 100
        return render(request, 'quiz_start.html', {"quiz": quiz,"percentage":percentage, "score":score, "questions":questions, "attempted":  attempted, "remaining_time_sec":remaining_time_sec, "responses": user_response})

    return render(request, 'quiz_start.html', {"quiz": quiz, "questions":questions, "attempted":  attempted, "remaining_time_sec":remaining_time_sec})
    

@login_required
@profile_completion_required()
@quiz_started()
def QuizSubmit(request, slug):
    user = request.user
    quiz = Quiz.objects.filter(slug=slug).first()
    questions = quiz.questions.all()

    attempted = QuizTaker.objects.filter(user=request.user.id,quiz=quiz.id).count() > 0

    quiz_taker_score = 0

    if (attempted):
        return redirect(reverse_lazy("quiz_start", args=(quiz.slug,)))
    else:
        responses = []
        for question in questions:

            try:
                q_id = question.id
                correct_option = question.options.filter(is_answer=True).first()
                # correct_option_id = correct_option.id
                user_response = request.POST.get(str(q_id))
                user_option = question.options.filter(id = int(user_response)).first()
            
                
                if(correct_option.id == user_option.id):
                    quiz_taker_score += 1
                    is_correct = True
                else:
                    is_correct = False
                    
                
                responses.append(
                    Response(
                        user = user,
                        quiz = quiz,
                        question = question,
                        option = user_option,
                        correct_option = correct_option,
                        is_correct = is_correct
                    )
                )
            except:
                # user not attempted this question.
                responses.append(
                    Response(
                        user = user,
                        quiz = quiz,
                        question = question,
                        option = None,
                        correct_option = correct_option,
                        is_correct = False
                    )
                )
            
        quiz_take = QuizTaker.objects.create(
            user = user,
            quiz = quiz,
            score = quiz_taker_score
        )

        Response.objects.bulk_create(responses)
  
        return redirect(reverse_lazy("home_page"))


def leaderboard(request):
    user_model = get_user_model()

   
    top_scorers = user_model.objects.annotate(quiz_count=Count("quiz_takers"),score=Sum("quiz_takers__score")).order_by("-quiz_count","-score")[:10]
    

    top_participations = user_model.objects.annotate(quiz_count=Count("quiz_takers")).order_by('-quiz_count')[:10]
        
    context = {
        "top_participations": top_participations,
        "top_scorers": top_scorers,
    }
    return render(request, "leaderboard.html", context)




def quiz_leaderboard(request, slug):
    quiz = Quiz.objects.filter(slug=slug).first()


    top_scorers = QuizTaker.objects.filter(quiz=quiz).order_by("-score","completion_time")[:10]
        
    context = {
        "top_scorers": top_scorers,
        "quiz": quiz,
    }
    return render(request,'quiz_leaderboard.html', context)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Course, Lesson, Enrollment, Question, Choice, Submission

class CourseListView(generic.ListView):
    template_name = 'onlinecourse/course_list.html'
    context_object_name = 'course_list'
    def get_queryset(self): return Course.objects.order_by('-pub_date')[:10]

class CourseDetailView(generic.DetailView):
    model = Course
    template_name = 'onlinecourse/course_details_bootstrap.html'

def enroll(request, course_id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        Enrollment.objects.get_or_create(user=request.user, course=course)
        return HttpResponseRedirect(reverse('onlinecourse:course_details', args=(course.id,)))

def submit(request, course_id):
    if request.method == 'POST' and request.user.is_authenticated:
        course = get_object_or_404(Course, pk=course_id)
        enrollment = get_object_or_404(Enrollment, user=request.user, course=course)
        selected_choice_ids = [int(bid) for bid in request.POST.getlist('choice')]
        submission = Submission.objects.create(enrollment=enrollment)
        for choice_id in selected_choice_ids:
            choice = get_object_or_404(Choice, pk=choice_id)
            submission.choices.add(choice)
        return HttpResponseRedirect(reverse('onlinecourse:show_exam_result', args=(course.id, submission.id)))

def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)
    total_grade = 0
    user_score = 0
    for question in course.question_set.all():
        total_grade += question.grade
        if question.is_get_score([c.id for c in submission.choices.all()]):
            user_score += question.grade
    percentage = (user_score / total_grade) * 100 if total_grade > 0 else 0
    context = {
        'course': course, 'submission': submission, 'total_grade': total_grade,
        'user_score': user_score, 'percentage': percentage, 'passed': percentage >= 70
    }
    return render(request, 'onlinecourse/exam_result_bootstrap.html', context)
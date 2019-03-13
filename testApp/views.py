from quiz_App import settings

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from django.db.models import Sum
import simplejson, json
from . import models
import random


class StartTest(View):
    template_name = 'testApp/index.html'

    def get(self, request, test_id):
        request.session['Test_ID'] = test_id
        test = models.TestTable.objects.get(id=test_id)
        return render(request, self.template_name, {
            'test': test
        })


class QuestionsSlide(View):
    template_name = 'testApp/QuestionSlide.html'

    def get(self, request, test_id):
        questions = []
        test = models.TestTable.objects.get(id=test_id)
        ts = models.TestSubjectTable.objects.filter(Test__id=test.id)
        ut = models.UserTestQuestionJunction.objects.filter(UserTest__Test__id=test_id)
        if ut.count() > 0:
            for u in ut:
                q = models.QuestionsTable.objects.get(id=u.question.id)
                questions.append(q)
        else:
            for subject_wise in ts:
                sub_questions = models.QuestionsTable.objects.filter(Subject=subject_wise.Subject)
                for que in sub_questions:
                    questions.append(que)
        random.shuffle(questions)
        questions = questions[0:test.Number_of_Questions]
        # questions = models.QuestionsTable.objects.filter(Test_Name=test).order_by('Subject__Subject_name')
        Data_array = []
        subject_id_array = []
        subject_array = []
        count = 0
        time_remaining = test.Time_allotted
        for question in questions:
            if question.Subject.id not in subject_id_array:
                subject_id_array.append(question.Subject.id)
                subject_array.append((question.Subject.Subject_name, count))
            count = count + 1
            question_array = []  # [q_id, q_text, q_img, op_1, op_2, op_3, op_4, selected option, Time taken, Subject Name, marked]
            question_array.append(question.id)
            question_array.append(str(question.Question))
            try:
                question_array.append(question.Question_Image.url)
            except Exception as e:
                question_array.append('')
            question_array.append(question.Option_1)
            question_array.append(question.Option_2)
            question_array.append(question.Option_3)
            question_array.append(question.Option_4)
            try:
                utqj = models.UserTestQuestionJunction.objects.get(UserTest__Test=test, UserTest__Student__username=request.user, question__id=question.id)
                question_array.append(utqj.option_selected)                            # selected option
                question_array.append(utqj.timetaken)                                  # Time taken
                time_remaining = time_remaining - utqj.timetaken
            except Exception as e:
                question_array.append(5)                            # selected option
                question_array.append(0)                            # Time taken
            question_array.append(question.Subject.Subject_name)
            try:
                if utqj.result == 4:
                    question_array.append('y')  # Marked y/n
                else:
                    question_array.append('n')
            except Exception as e:
                question_array.append('n')  # Marked y/n
            Data_array.append(question_array)
        return render(request, self.template_name, {
            'test': test,
            'Data_array': simplejson.dumps(Data_array),
            'range': range(0, len(Data_array)),
            'subject_count': ts.count(),
            'time_remaining': time_remaining,
            'subject_array': subject_array
        })


class CompleteTest(View):
    template_name = 'testApp/CompleteTest.html'

    def post(self, request):
        Data_array = json.loads(request.POST['json_container'])
        user = User.objects.get(username=request.user)
        test = models.TestTable.objects.get(id=request.session['Test_ID'])
        try:
            # If entries are already present (Resume test scenario)
            utj = models.UserTestJunction.objects.get(Student=user, Test=test)
            for row in Data_array:
                utqj = models.UserTestQuestionJunction.objects.get(UserTest=utj, question__id=row[0])
                utqj.timetaken = row[8]
                utqj.option_selected = row[7]
                if int(utqj.question.Correct_option) == int(utqj.option_selected):
                    utqj.result = 1 # code for correct answer
                else:
                    if int(utqj.option_selected) > 4:
                        utqj.result = 2   #code for unanswered Questions
                    else:
                        utqj.result = 3  # code for wrong answer
                    if row[10] == 'y' or row[10] == 'yy':
                        utqj.result = 4  # code for marked Questions
                utqj.save()
        except Exception as e:
            # The entries are added for the first time
            utj = models.UserTestJunction(Student=user, Test=test)
            utj.save()
            for row in Data_array:
                utqj = models.UserTestQuestionJunction(UserTest=utj)
                utqj.question = models.QuestionsTable.objects.get(id=row[0])
                utqj.timetaken = row[8]
                utqj.option_selected = row[7]
                if int(utqj.question.Correct_option) == int(utqj.option_selected):
                    utqj.result = 1 # code for correct answer
                else:
                    if int(utqj.option_selected) > 4:
                        utqj.result = 2   #code for unanswered Questions
                    else:
                        utqj.result = 3  # code for wrong answer
                utqj.save()
        try:
            if request.POST['complete_test'] == 'on':
                utqj = models.UserTestQuestionJunction.objects.filter(UserTest=utj)
                utj.Status = 'completed'
                Total_questions = test.Number_of_Questions
                Total_marks = Total_questions*test.Positive_mark
                no_of_correct_answer = utqj.filter(result=1).count()
                no_of_unanswered_answer = utqj.filter(result=2).count()
                no_of_wrong_answer = utqj.filter(result=3).count()
                total_time_taken = utqj.aggregate(Sum('timetaken'))
                obtained_marks = (no_of_correct_answer*test.Positive_mark)-(no_of_wrong_answer*test.Negative_mark)
                user_percentage = obtained_marks/Total_marks * 100
                required_marks = test.Pass_percentage
                # to calculate subject wise data
                subject_wise_marks = []
                subject_array = set(utqj.values_list('question__Subject', flat=True))
                for subject_id in subject_array:
                    subject_data = utqj.filter(question__Subject=subject_id)
                    subject_wise_marks.append((models.SubjectsTable.objects.get(id=subject_id),
                                              subject_data.filter(result=1).count()*test.Positive_mark,
                                              subject_data.filter(result=1).count(),
                                              subject_data.filter(result=3).count(),
                                              subject_data.aggregate(Sum('timetaken')),
                                               ))
                if user_percentage > required_marks:
                    utj.result = 'pass'
                else:
                    utj.result = 'fail'
                utj.save()
                return render(request, self.template_name, {
                    'total_marks_obtained': obtained_marks,
                    'total_time_taken': total_time_taken,
                    'subject_wise_marks': subject_wise_marks,
                    'obtained_percentage': user_percentage,
                    'wrong_marks': no_of_wrong_answer*test.Negative_mark,
                    'Total_marks': Total_marks,
                    'obtained_marks': obtained_marks
                })
        except Exception as e:
            return render(request, 'testApp/close_js.html')

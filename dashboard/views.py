from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.models import User
from testApp import models


class HomePageView(View):
    template_name = 'dashboard/HomePage.html'

    def get(self, request):
        user_object = User.objects.get(username=request.user)
        test_status_string = None
        testbatch = None
        if user_object.is_staff:
            all_tests = models.TestTable.objects.all()
            test_status_string = self.check_status(all_tests)
            is_admin = True
        else:
            batch_object = models.UserExtensionTable.objects.filter(Student=user_object)
            testbatch = []
            for batch in batch_object:
                testbatch_1 = models.TestBatchJunction.objects.filter(Batch=batch.Batch, Test__Test_Ready=True)
                for tb in testbatch_1:
                    if not models.UserTestJunction.objects.filter(Test=tb.Test, Student=user_object):
                        testbatch.append(tb)
            is_admin = False
        return render(request, self.template_name, {
                        'testbatch': testbatch,
                        'is_admin': is_admin,
                        'test_status_string': test_status_string
        })

    def post(self, request):
        return HomePageView.get(self, request)

    def check_status(self, all_tests):
        test_status_string = []  # (Test name , Status Description, Status )
        for test in all_tests:
            test_mini_string = []
            all_test_subjects = models.TestSubjectTable.objects.filter(Test=test)
            test_mini_string.append(test.Test_Name)
            status_fail = False
            status_string = ''
            has_data = False
            for ts in all_test_subjects:
                has_data =True
                required_count = ts.sub_wise_number_of_questions
                available_count = models.QuestionsTable.objects.filter(Subject=ts.Subject).count()
                status_string = status_string + ts.Subject.Subject_name + ' : ' + str(available_count) \
                                + '/' + str(required_count) + ' '
                if not required_count <= available_count:
                    status_fail = True
            if not has_data:
                status_string = 'You havent added Subject wise Split Up'
                status_fail = True
            test_mini_string.append(status_string)
            if status_fail:
                test_mini_string.append('Test Not Ready')
            else:
                test_mini_string.append('Test Ready')
            test_status_string.append(test_mini_string)
        return test_status_string


class MyTestView(View):

    def get(self, request):
        user = User.objects.get(username=request.user)
        all_taken_tests = models.UserTestJunction.objects.filter(Student=user)
        print(all_taken_tests)
        return render(request, 'dashboard/mytests.html', {
            'all_tests': all_taken_tests
        })


class TestQuestionsView(View):

    def get(self, request, test_id):
        test = models.TestTable.objects.get(id=test_id)
        user = User.objects.get(username=request.user)
        utj = models.UserTestJunction.objects.get(Student=user, Test=test)
        utqj = models.UserTestQuestionJunction.objects.filter(UserTest=utj)
        bookmarks = models.BookmarksTable.objects.filter(Student=user)
        bookmark_list = []
        for bookmark in bookmarks:
            bookmark_list.append(bookmark.bookmarked_question.id)
        total_time_spent = 0
        subject_wise_array = []
        for question in utqj:
            total_time_spent = total_time_spent + question.timetaken
        subject_list = set(utqj.values_list('question__Subject', flat=True))
        for sub_id in subject_list:
            subject = models.SubjectsTable.objects.get(id=sub_id)
            query = models.UserTestQuestionJunction.objects.filter(question__Subject=subject)
            total_number_of_subject_questions = query.count()
            correct_number_of_subject_questions = query.filter(result=1).count()
            incorrect_number_of_subject_questions = query.filter(result=3).count()
            positive_marks = correct_number_of_subject_questions*test.Positive_mark
            negative_marks = incorrect_number_of_subject_questions*test.Negative_mark
            subject_wise_array.append([subject.Subject_name,
                                       total_number_of_subject_questions,
                                       correct_number_of_subject_questions,
                                       incorrect_number_of_subject_questions,
                                       positive_marks,
                                       negative_marks,
                                       positive_marks-negative_marks
                                       ])
        #    subject_wise_array.append([subject.Subject_name, subject])
        Total_marks = test.Number_of_Questions*test.Positive_mark
        no_of_correct_answer = utqj.filter(result=1).count()
        no_of_unanswered_answer = utqj.filter(result=2).count()
        no_of_wrong_answer = utqj.filter(result=3).count()
        obtained_marks = (no_of_correct_answer * test.Positive_mark) - (no_of_wrong_answer * test.Negative_mark)
        return render(request, 'dashboard/testquestions.html', {
            'all_questions_utqj': utqj,
            'test_id': test_id,
            'bookmark_list': bookmark_list,
            'Total_marks': Total_marks,
            'Total_time': test.Time_allotted/60,
            'Total_questions': test.Number_of_Questions,
            'user_marks': obtained_marks,
            'total_time_spent_min': int(total_time_spent/60),
            'total_time_spent_sec': int(total_time_spent % 60),
            'Total_correct': no_of_correct_answer,
            'Total_incorrect': no_of_wrong_answer,
            'Total_unanswered': no_of_unanswered_answer,
            'percentage_scored': obtained_marks/Total_marks*100,
            'subject_wise_array': subject_wise_array
        })


class AddBookmarkView(View):

    def get(self, request, test_id):
        user = User.objects.get(username=request.user)
        bookmark = models.BookmarksTable()
        bookmark.Student = user
        question = models.QuestionsTable.objects.get(id=int(request.GET['question_id']))
        bookmark.bookmarked_question = question
        try:
            bookmark.doubt_description = self.request.GET['doubt_description']
        except Exception as e:
            bookmark.doubt_description = ''
        bookmark.save()
        return redirect('dashboard:testquestions', test_id)


class RemoveBookmarkView(View):

    def get(self, request, question_id):
        models.BookmarksTable.objects.get(id=question_id).delete()
        return redirect('dashboard:bookmarklist')


class BookMarkListView(View):

    def get(self, request):
        user = User.objects.get(username=request.user)
        Data_array = []
        bookmarks = models.BookmarksTable.objects.filter(Student=user)
        Data_array.append(['All Questions', bookmarks])
        subject_id_list = set(bookmarks.values_list('bookmarked_question__Subject__id', flat=True))
        for ids in subject_id_list:
            print('here')
            bookmarks_array = bookmarks.filter(bookmarked_question__Subject__id=ids)
            subject_name = bookmarks_array[0].bookmarked_question.Subject.Subject_name
            Data_array.append([subject_name, bookmarks_array])
        return render(request, 'dashboard/bookmarkslist.html', {
            'Data_array': Data_array
        })


class ProfileView(View):

    def get(self, request):
        user = models.User.objects.get(username=request.user)
        batch_list = models.UserExtensionTable.objects.filter(Student=user)
        return render(request, 'dashboard/profile.html', {
            'user': user,
            'batch_list': batch_list
        })


class AboutUs(View):

    def get(self, request):
        return render(request, 'dashboard/aboutus.html')


class CustomAdmin(View):

    def get(self, request):
        student_list = models.User.objects.filter()
        batch_list = models.BatchTable.objects.filter()
        return render(request, 'dashboard/custom_admin.html', {
                    'student_list': student_list,
                    'batch_list': batch_list,
                    'msg': ''
        })

    def post(self, request):
        batch = models.BatchTable.objects.get(id=int(request.POST['batch']))
        for student_id in request.POST.getlist('student_list'):
            user = models.User.objects.get(id=int(student_id))
            models.UserExtensionTable(Student=user, Batch=batch).save()
        student_list = models.User.objects.filter()
        batch_list = models.BatchTable.objects.filter()
        return render(request, 'dashboard/custom_admin.html', {
            'student_list': student_list,
            'batch_list': batch_list,
            'msg': 'successfully added!!'
        })

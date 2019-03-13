from django.db import models
from django.contrib.auth.models import User


class BatchTable(models.Model):
    Batch_Name = models.CharField(max_length=50, null=False, unique=True)

    def __str__(self):
        return self.Batch_Name


class UserExtensionTable(models.Model):
    Student = models.ForeignKey(User, null=False, on_delete='CASCADE')
    Batch = models.ForeignKey(BatchTable, null=False, on_delete='CASCADE')

    def __str__(self):
        return self.Student.username + ' - - - - - ' + self.Batch.Batch_Name


class SubjectsTable(models.Model):
    Subject_name = models.CharField(max_length=100, null=False, unique=True)

    def __str__(self):
        return self.Subject_name


class TestTable(models.Model):
    category = (
        ('Single Subject', 'Single Subject'),
        ('Multi Subject', 'Multi Subject')
    )
    Test_Name = models.CharField(max_length=250, null=False, unique=True)
    Test_category = models.CharField(max_length=250, choices=category, null=False)
    Number_of_Questions = models.IntegerField()
    Time_allotted = models.IntegerField()
    Pass_percentage = models.IntegerField(default=35)
    Test_Ready = models.BooleanField(default=False)
    Positive_mark = models.FloatField(default=1.0)
    Negative_mark = models.FloatField(default=0.25)

    def __str__(self):
        return self.Test_Name
               # + ' Test Category: ' + self.Test_category + \
               # ' number of Questions' + str(self.Number_of_Questions) + 'Time Alloted' + str(self.Time_allotted)


class TestSubjectTable(models.Model):
    Test = models.ForeignKey(TestTable, on_delete='CASCADE')
    Subject = models.ForeignKey(SubjectsTable, on_delete='CASCADE')
    sub_wise_number_of_questions = models.IntegerField()

    def __str__(self):
        return str(self.Subject.id) + self.Test.Test_Name + ' has total of ' + str(self.Test.Number_of_Questions) \
               + ' questions. in this ' + self.Subject.Subject_name + ' has '\
               + str(self.sub_wise_number_of_questions)


class TestBatchJunction(models.Model):
    Test = models.ForeignKey(TestTable, null=False, on_delete='CASCADE')
    Batch = models.ForeignKey(BatchTable, null=False, on_delete='CASCADE')

    def __str__(self):
        return self.Test.Test_Name + ' --------------- ' + self.Batch.Batch_Name


class QuestionsTable(models.Model):
    Subject = models.ForeignKey(SubjectsTable, null=False, on_delete='CASCADE')
    Question = models.TextField(max_length=500, null=False)
    Question_Image = models.ImageField(null=True, blank=True)
    Option_1 = models.CharField(max_length=500, null=False)
    Option_2 = models.CharField(max_length=500, null=False)
    Option_3 = models.CharField(max_length=500, null=False)
    Option_4 = models.CharField(max_length=500, null=False)
    choices = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    )
    Correct_option = models.IntegerField(choices=choices)
    Solution_Explanation = models.TextField(null=False, max_length=1000)

    def __str__(self):
        return self.Subject.Subject_name + ' ---------- ' + str(self.Question)


class UserTestJunction(models.Model):
    Student = models.ForeignKey(User, null=False, on_delete='CASCADE')
    Test = models.ForeignKey(TestTable, null=False, on_delete='CASCADE')
    Status = models.CharField(max_length=200, default='inp')
    result = models.CharField(max_length=200, default='fail')

    def __str__(self):
        return self.Student.username + ' -------- ' + self.Test.Test_Name


class UserTestQuestionJunction(models.Model):
    UserTest = models.ForeignKey(UserTestJunction, on_delete='CASCADE')
    question = models.ForeignKey(QuestionsTable, on_delete='CASCADE')
    timetaken = models.IntegerField()
    option_selected = models.IntegerField()
    result = models.IntegerField()

    def __str__(self):
        return self.UserTest.Student.username + ' || ' + self.question.Question + ' || ' + str(self.result)


class BookmarksTable(models.Model):
    Student = models.ForeignKey(User, on_delete='CASCADE')
    bookmarked_question = models.ForeignKey(QuestionsTable, on_delete='CASCADE')
    doubt_description = models.TextField(null=True, max_length=1000)







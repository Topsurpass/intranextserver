from django.urls import path
from .views import (
    ExamDetailView, 
    SubmitExamView,
    ExamListView,
    UserCourseScoreView,
    CompletedCoursesWithScoresView,
    AvailableExamsView,
    ReviewExamView
    )

examurlpatterns = [
    path('exams/', ExamListView.as_view(), name='exam-lists'),
    path('exam/<uuid:pk>/', ExamDetailView.as_view(), name='exam-detail'),
    path('exam/submit/', SubmitExamView.as_view(), name='submit-exam'),
    path('course/<uuid:course_id>/user-score/', UserCourseScoreView.as_view(), name='user-course-score'),
    path('completed-courses/', CompletedCoursesWithScoresView.as_view(), name='completed-courses'),
    path('available-exams/', AvailableExamsView.as_view(), name='available-exams'),
    path('exam/<uuid:exam_id>/review/', ReviewExamView.as_view(), name='exam-review'),
]

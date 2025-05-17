from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Exam, ExamSubmission
from .serializers import ExamSerializer, ExamSubmissionSerializer
from rest_framework.views import APIView
from django.db.models import Avg

class ExamListView(generics.ListAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]

class ExamDetailView(generics.RetrieveAPIView):
    queryset = Exam.objects.all()
    serializer_class = ExamSerializer
    permission_classes = [IsAuthenticated]


class SubmitExamView(generics.GenericAPIView):
    serializer_class = ExamSubmissionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ExamSubmissionSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        result = serializer.save()
        return Response(result, status=status.HTTP_200_OK)


class UserCourseScoreView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, course_id):
        user = request.user

        exams_in_course = Exam.objects.filter(course_id=course_id)

        submissions = ExamSubmission.objects.filter(user=user, exam__in=exams_in_course)

        if submissions.exists():
            average_score = submissions.aggregate(avg_score=Avg('score'))['avg_score']
        else:
            average_score = None

        # Return detailed or summary info
        return Response({
            'course_id': course_id,
            'user_id': user.id,
            'average_score': average_score,
            'submissions': [
                {
                    'exam_id': s.exam.id,
                    'exam_title': s.exam.title,
                    'score': s.score,
                    'submitted_at': s.submitted_at,
                } for s in submissions
            ]
        })
    

class CompletedCoursesWithScoresView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        submissions = ExamSubmission.objects.filter(user=user).select_related('exam__course')

        course_map = {}
        total_score_sum = 0
        total_possible_score = 0

        for submission in submissions:
            course = submission.exam.course
            exam = submission.exam

            if course.id not in course_map:
                course_map[course.id] = {
                    'course_id': course.id,
                    'course_title': course.title,
                    'course_description': course.description,
                    'exams': [],
                    'total_score': 0,
                    'exam_count': 0,
                    'average_score': 0,
                }

            course_data = course_map[course.id]
            course_data['exams'].append({
                'exam_id': exam.id,
                'exam_title': exam.title,
                'score': submission.score,
                'submitted_at': submission.submitted_at,
                'duration': exam.duration
            })

            course_data['total_score'] += submission.score
            course_data['exam_count'] += 1

            total_score_sum += submission.score
            total_possible_score += 100

        for course in course_map.values():
            if course['exam_count'] > 0:
                course['average_score'] = round(course['total_score'] / course['exam_count'], 2)
            else:
                course['average_score'] = 0

            del course['total_score']
            del course['exam_count']

        overall_average = round(total_score_sum / total_possible_score * 100, 2) if total_possible_score > 0 else 0

        return Response({
            'overall_average_score': overall_average,
            'completed_courses': list(course_map.values())
        })

    
class AvailableExamsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        submitted_exam_ids = ExamSubmission.objects.filter(user=user).values_list('exam_id', flat=True)

        available_exams = Exam.objects.exclude(id__in=submitted_exam_ids).select_related('course')

        exams_data = []
        for exam in available_exams:
            exams_data.append({
                'exam_id': exam.id,
                'exam_title': exam.title,
                'description':exam.description,
                'duration': exam.duration,
                'course_id': exam.course.id,
                'course_title': exam.course.title,
                'course_description': exam.course.description,
            })

        return Response(exams_data)

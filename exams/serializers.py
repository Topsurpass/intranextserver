from rest_framework import serializers
from .models import Exam, Question, Option, ExamSubmission, UserAnswer
from rest_framework.exceptions import NotFound, ValidationError


class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text']

class QuestionSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'text', 'options']


class ExamSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exam
        fields = ['id', 'title', 'description', 'duration', 'questions']

class UserAnswerSerializer(serializers.Serializer):
    question = serializers.UUIDField()
    selected_option = serializers.UUIDField()


class ExamSubmissionSerializer(serializers.Serializer):
    exam_id = serializers.UUIDField()
    answers = serializers.ListSerializer(child=UserAnswerSerializer())

    def validate(self, data):
        exam_id = data['exam_id']
        question_ids = [item['question'] for item in data['answers']]
        
        invalid_questions = Question.objects.exclude(
            id__in=question_ids
        ).filter(exam_id=exam_id)

        if invalid_questions.exists():
            raise serializers.ValidationError("One or more questions do not belong to the specified exam.")
        
        return data

    def create(self, validated_data):
        user = self.context['request'].user
        exam_id = validated_data['exam_id']
        answers = validated_data['answers']

        try:
            exam = Exam.objects.get(id=exam_id)
        except Exam.DoesNotExist:
            raise NotFound("The exam with the given ID does not exist.")

        if ExamSubmission.objects.filter(user=user, exam=exam).exists():
            raise ValidationError("You have already submitted this exam.")

        total_questions = exam.questions.count()
        correct = 0

        submission = ExamSubmission.objects.create(user=user, exam=exam, score=0)

        for answer in answers:
            q_id = answer['question']
            selected_option_id = answer['selected_option']

            try:
                option = Option.objects.get(id=selected_option_id, question_id=q_id)
                question = Question.objects.get(id=q_id)

                UserAnswer.objects.create(
                    submission=submission,
                    question=question,
                    selected_option=option
                )

                if option.is_correct:
                    correct += 1

            except Option.DoesNotExist:
                continue

        score = round((correct / total_questions) * 100, 2)
        submission.score = score
        submission.save()

        return {'score': score, 'submitted': True}


class ReviewedOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'is_correct']


class ReviewedQuestionSerializer(serializers.ModelSerializer):
    options = ReviewedOptionSerializer(many=True, read_only=True)
    selected_option_id = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ['id', 'text', 'options', 'selected_option_id']

    def get_selected_option_id(self, question):
        user_answers = self.context.get('user_answers', {})
        return user_answers.get(str(question.id)) 
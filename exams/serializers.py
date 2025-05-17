from rest_framework import serializers
from .models import Exam, Question, Option, ExamSubmission


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
        exam = Exam.objects.get(id=validated_data['exam_id'])
        answers = validated_data['answers']

        if ExamSubmission.objects.filter(user=user, exam=exam).exists():
            raise serializers.ValidationError("You have already taken this exam.")

        total_questions = exam.questions.count()
        correct = 0

        for answer in answers:
            q_id = answer['question']
            selected_option_id = answer['selected_option']
            try:
                option = Option.objects.get(id=selected_option_id, question_id=q_id)
                if option.is_correct:
                    correct += 1
            except Option.DoesNotExist:
                continue

        score = round((correct / total_questions) * 100, 2)

        submission, created = ExamSubmission.objects.update_or_create(
            user=user,
            exam=exam,
            defaults={'score': score}
        )
        return {'score': score, 'submitted': created}

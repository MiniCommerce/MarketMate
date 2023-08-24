from rest_framework import serializers
from .models import Question
from products.models import Product


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = '__all__'

    def get_answer(self, instance):
        answers = instance.answer.all()
        serializer = QuestionSerializer(answers, many=True)
        
        return serializer.data
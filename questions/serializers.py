from rest_framework import serializers
from .models import Question
from products.models import Product


class QuestionSerializer(serializers.ModelSerializer):
    answer = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = ('product', 'id', 'user', 'desc', 'parent', 'created_at', 'answer')
        # fields = '__all__'

    def get_answer(self, instance):
        serializer = self.__class__(instance.answer, many=True)
        serializer.bind('', self)
        return serializer.data
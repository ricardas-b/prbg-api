from django import forms

from api_app.models import Quote, Tag


class QuoteForm(forms.ModelForm):
    class Meta:
        model = Quote
        fields = '__all__'
        exclude = ('editors_comment', 'length_in_words', 'rating', )


class TagsForm(forms.Form):
    tags = None

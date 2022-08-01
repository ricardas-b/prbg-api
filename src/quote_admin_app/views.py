import django

from django.shortcuts import redirect, render

from . import forms
from api_app.models import Quote, QuoteTag, Tag



def show_quote_with_tags(request, pk):
    if request.method == 'GET':

        # Quote form
        quote = Quote.objects.get(pk=pk)
        quote_form = forms.QuoteForm(instance=quote)

        # Tag form
        all_tags = Tag.objects.values('pk', 'name').order_by('name')
        all_tags = [list(tag.values()) for tag in all_tags]

        selected_tags = list(QuoteTag.objects.filter(quote=pk).values())
        selected_tags = [tag['tag_id'] for tag in selected_tags]

        selected_tag_values = []

        for tag in all_tags:
            if tag[0] in selected_tags:
                tag.append(True)
                selected_tag_values.append(tag[1])
            else:
                tag.append(False)

        selected_tag_values = ', '.join(selected_tag_values)

        context = {
            'pk': pk,
            'quote_form': quote_form,
            'all_tags': all_tags,
            'selected_tag_values': selected_tag_values,
        }

        return render(request, 'quote_template.html', context)


def update_quote(request, pk):
    if request.method == 'POST':
        quote = Quote.objects.get(pk=pk)
        quote_form = forms.QuoteForm(request.POST, instance=quote)
        quote_form.save()
        return redirect(f'/api/v1/show-quote/{pk}/')


def update_tags(request, pk):
    if request.method == 'POST':

        old_tag_selection = [tag['tag_id'] for tag in QuoteTag.objects.filter(quote=pk).values()]
        new_tag_selection = list(request.POST.getlist('tag_selection'))
        new_tag_selection = [int(i) for i in new_tag_selection]

        for tag_id in new_tag_selection:
            if tag_id not in old_tag_selection:
                quote = Quote.objects.get(pk=pk)
                tag = Tag.objects.get(pk=tag_id)
                QuoteTag(quote=quote, tag=tag).save()

        for tag_id in old_tag_selection:
            if tag_id not in new_tag_selection:
                QuoteTag.objects.get(quote=pk, tag=tag_id).delete()

        return redirect(f'/api/v1/show-quote/{pk}/')



from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from review_assign.forms import SubmitAssingmentInformation
from django.views.generic import FormView
from django.http import HttpResponseRedirect, HttpResponse
import django_tables2 as tables
from django_tables2 import RequestConfig
from django.core.urlresolvers import reverse
import pandas as pd

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from utils import get_file_path

from review_assign.tasks import LinearProgrammingAssignment

def docs(request):
    return render_to_response('review_assign/docs_review_assign.html')


class index(FormView):
    template_name = 'review_assign/submit.html'
    form_class = SubmitAssingmentInformation

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            people_pd = pd.read_csv(form.cleaned_data['people'], index_col=None)
            article_pd = pd.read_csv(form.cleaned_data['article_information'], index_col=None)
            reviewer_pd = pd.read_csv(form.cleaned_data['reviewers'], index_col=None)
            min_rev_art = form.cleaned_data['minimum_reviews_per_article']
            max_rev_art = form.cleaned_data['maximum_reviews_per_article']
            min_art_rev = form.cleaned_data['minimum_articles_per_reviewer']
            max_art_rev = form.cleaned_data['maximum_articles_per_reviewer']

            task = LinearProgrammingAssignment.delay_or_fail(reviewer_abstracts=reviewer_pd.Abstract.tolist(),
                                                       article_data=article_pd.to_dict(),
                                                       people_data=people_pd.to_dict(),
                                                       min_rev_art=min_rev_art,
                                                       max_rev_art=max_rev_art,
                                                       min_art_rev=min_art_rev,
                                                       max_art_rev=max_art_rev)

            return render_to_response('progress.html',
                                      {'task_id': task.task_id,
                                       'progress_title': 'Solving the assignment problem',
                                       'result_view': 'result',
                                       'start_over_view': 'review_assign_index'})
        else:
            return self.form_invalid(form)


class PeopleTable(tables.Table):
    PersonID = tables.Column(verbose_name='ID')
    FullName = tables.Column(verbose_name='Full name')


class AssignmentTable(tables.Table):
    PaperID = tables.Column()
    Title = tables.Column()
    Reviewers = tables.Column()

def result(request, task_id=None):
    # read from celery the results
    # save CSV file
    from reviewer_assignment_website import celery_app
    from StringIO import StringIO
    task_results = celery_app.AsyncResult(task_id).get()
    assignment_df = pd.read_csv(StringIO(task_results))
    assignment_df = assignment_df.fillna('')
    reviewer_assignments_table = AssignmentTable(assignment_df.to_dict('records'))
    config = RequestConfig(request)
    config.paginate = False
    config.configure(reviewer_assignments_table)
    return render_to_response('review_assign/result.html',
                              {"reviewer_assignments": reviewer_assignments_table,
                               "task_id": task_id},
                              context_instance=RequestContext(request))

def download_result(_, task_id=None):
    import os
    from django.core.servers.basehttp import FileWrapper
    from django.conf import settings
    import mimetypes
    from reviewer_assignment_website import celery_app
    from StringIO import StringIO

    task_results = celery_app.AsyncResult(task_id).get()

    download_name = 'result_%s.csv' % task_id
    wrapper = FileWrapper(StringIO(task_results))
    content_type = mimetypes.guess_type(download_name)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = len(task_results)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name
    return response

import pandas as pd
from StringIO import StringIO
import mimetypes

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import FormView
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

import django_tables2 as tables

from review_scoring.forms import SubmitScoreInformation
from review_scoring.tasks import ArticleScoring

from reviewer_assignment_website import celery_app


def docs(_):
    return render_to_response('review_scoring/docs_review_scoring.html')


class Index(FormView):
    template_name = 'review_scoring/submit.html'
    form_class = SubmitScoreInformation

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            # print request.FILES['scores'].read()
            scores = pd.DataFrame.from_csv(StringIO(request.FILES['scores'].read()),
                                           index_col=None)

            task = ArticleScoring.delay_or_fail(scores=scores.to_dict())

            return render_to_response('progress.html',
                                      {'task_id': task.task_id,
                                       'progress_title': 'Estimating article scores',
                                       'result_view': 'result_scoring',
                                       'start_over_view': 'review_scoring_index'})
        else:
            return self.form_invalid(form)


class ScoringTable(tables.Table):
    PaperID = tables.Column()
    Mean = tables.Column(verbose_name='Mean score')
    SD = tables.Column(verbose_name='Uncertainty')


def result(request, task_id=None):
    # read from celery the results
    # save CSV file
    task_results = celery_app.AsyncResult(task_id).get()
    scoring_df = pd.read_csv(StringIO(task_results))
    scoring_df = scoring_df.fillna('')
    scoring_results_table = ScoringTable(scoring_df.to_dict('records'))
    return render_to_response('review_scoring/result.html',
                              {"scoring_results": scoring_results_table,
                               "task_id": task_id},
                              context_instance=RequestContext(request))


def download_result(_, task_id=None):
    task_results = celery_app.AsyncResult(task_id).get()

    download_name = 'result_%s.csv' % task_id
    wrapper = FileWrapper(StringIO(task_results))
    content_type = mimetypes.guess_type(download_name)[0]
    response = HttpResponse(wrapper, content_type=content_type)
    response['Content-Length'] = len(task_results)
    response['Content-Disposition'] = "attachment; filename=%s" % download_name
    return response
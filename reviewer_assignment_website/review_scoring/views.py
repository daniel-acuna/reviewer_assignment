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

import numpy as np
import mpld3
import matplotlib
import matplotlib.mlab as mlab
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas


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

    class Meta:
        attrs = {'class': 'score_table_style'}


def result(request, task_id=None):
    # read from celery the results
    # save CSV file
    task_results = celery_app.AsyncResult(task_id).get()
    scoring_df = pd.read_csv(StringIO(task_results))
    scoring_df = scoring_df.fillna('')
    scoring_results_table = ScoringTable(scoring_df.to_dict('records'))
    return render_to_response('review_scoring/result.html',
                              {"scoring_results": scoring_results_table,
                               "task_id": task_id,
                               "scoring_plot": create_html_plot_tooltip(scoring_df)},
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


class BayesView(mpld3.plugins.PluginBase):
    """class for plotting the Bayes scoring result"""

    JAVASCRIPT = """
    mpld3.register_plugin("linkedview", LinkedViewPlugin);
    LinkedViewPlugin.prototype = Object.create(mpld3.Plugin.prototype);
    LinkedViewPlugin.prototype.constructor = LinkedViewPlugin;
    LinkedViewPlugin.prototype.requiredProps = ["idpts", "idline", "data"];
    LinkedViewPlugin.prototype.defaultProps = {}
    function LinkedViewPlugin(fig, props){
        mpld3.Plugin.call(this, fig, props);
    };

    LinkedViewPlugin.prototype.draw = function(){
      var pts = mpld3.get_element(this.props.idpts);
      var line = mpld3.get_element(this.props.idline);
      var data = this.props.data;

      function mouseover(d, i){
        line.data = data[i];
        line.elements().transition()
            .attr("d", line.datafunc(line.data))
            .style("stroke", this.style.fill);
      }
      pts.elements().on("mouseover", mouseover);
    };
    """

    def __init__(self, points, line, linedata):
        if isinstance(points, matplotlib.lines.Line2D):
            suffix = "pts"
        else:
            suffix = None

        self.dict_ = {"type": "linkedview",
                      "idpts": mpld3.utils.get_id(points, suffix),
                      "idline": mpld3.utils.get_id(line),
                      "data": linedata}


def create_html_plot(scores_df):
    """
    Giving score dataframe, create a scatter html plot based on d3
    """
    fig, ax = plt.subplots(2)
    bayes_mean = np.array(scores_df['Mean'])
    bayes_sd = np.array(scores_df['SD'])
    x = np.linspace(np.min(bayes_mean)-2*np.max(bayes_sd),
                    np.max(bayes_mean)+2*np.max(bayes_sd), 100)
    data = np.array([[x, mlab.normpdf(x, bayes_mean_i, bayes_sd_i)]
                     for (bayes_mean_i, bayes_sd_i) in zip(bayes_mean, bayes_sd)])


def create_html_plot_tooltip(scores_df):
    """
    Giving score dataframe, create scatter plot with tooltip
    """
    css = """
    table, th, td
    {
      background-color: #FFFFFF;
      font-family:Lato;
    }
    """
    matplotlib.rcParams.update({'font.size': 20})
    fig = Figure()
    canvas = FigureCanvas(fig)
    ax = fig.add_subplot(111)
    bayes_mean = np.array(scores_df['Mean'])
    bayes_sd = np.array(scores_df['SD'])
    x = np.linspace(np.min(bayes_mean)-2*np.max(bayes_sd),
                    np.max(bayes_mean)+2*np.max(bayes_sd), 40)
    data = np.array([[x, mlab.normpdf(x, bayes_mean_i, bayes_sd_i)]
                     for (bayes_mean_i, bayes_sd_i) in zip(bayes_mean, bayes_sd)])

    scatter_plot = ax.scatter(bayes_mean, bayes_sd,
                           c=bayes_mean,
                           cmap='RdYlGn',
                           s=30, alpha=0.5)


    labels=[]
    scores_df.index = scores_df.PaperID.copy()
    del scores_df['PaperID']
    for i in range(len(scores_df)):
        label = scores_df.iloc[[i]]
        labels.append(str(label.to_html()))

    ax.set_xlabel('Mean Scores')
    ax.set_ylabel('Uncertainty')

    tooltip = mpld3.plugins.PointHTMLTooltip(scatter_plot,
                                              labels=labels,
                                              css=css,
                                              voffset=10,
                                              hoffset=10)
    mpld3.plugins.connect(fig, tooltip)
    return mpld3.fig_to_html(fig)
from jobtastic import JobtasticTask

import readline
import pandas as pd
import pandas.rpy.common as com
import rpy2.robjects as ro
from rpy2.robjects import pandas2ri
pandas2ri.activate()


class ArticleScoring(JobtasticTask):

    significant_kwargs = [
        ('scores', str),
    ]

    # How long should we give a task before assuming it has failed?
    herd_avoidance_timeout = 5*60  # Shouldn't take more than 60 seconds
    # How long we want to cache results with identical ``significant_kwargs``
    cache_duration = -1  # Cache these results forever. Math is pretty stable.
    # Note: 0 means different things in different cache backends. RTFM for yours.

    def calculate_result(self, scores):
        """
        Generates a csv file with the resulting assignment while it updates the status
        of the process using Celery
        """

        update_frequency = 1
        max_steps = 7
        self.update_progress(1, max_steps, update_frequency=update_frequency)
        ro.r('library(MASS)')
        self.update_progress(2, max_steps, update_frequency=update_frequency)
        ro.r('library(Matrix)')
        self.update_progress(3, max_steps, update_frequency=update_frequency)
        ro.r('library(lme4)')
        self.update_progress(4, max_steps, update_frequency=update_frequency)
        ro.r('library(Rcpp)')
        self.update_progress(5, max_steps, update_frequency=update_frequency)
        ro.r('library(arm)')
        self.update_progress(6, max_steps, update_frequency=update_frequency)

        scores_pd = pd.DataFrame(scores)
        # estimate scores
        rdf = com.convert_to_r_dataframe(scores_pd)
        ro.globalenv['scores'] = rdf

        if 'Confidence' in scores_pd.columns:
            fit_str = 'fit <- lmer(Score ~ 1 + (1 | PaperID) + (1 | PersonID), scores, weights = Confidence)'
        else:
            fit_str = 'fit <- lmer(Score ~ 1 + (1 | PaperID) + (1 | PersonID), scores)'

        ro.r(fit_str)

        ro.r('''bayes_score <- data.frame(PaperID = rownames(fixef(fit) + ranef(fit)$PaperID),
            Mean = (fixef(fit) + ranef(fit)$PaperID)[,1],
            SD = (se.ranef(fit)$PaperID)[, 1])''')

        bayes_score = pandas2ri.ri2py_dataframe(ro.r('bayes_score'))

        self.update_progress(7, max_steps, update_frequency=update_frequency)

        return bayes_score.to_csv(None, na_rep='', index=False, encoding='utf-8')

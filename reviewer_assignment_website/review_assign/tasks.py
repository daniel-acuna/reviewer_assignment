from jobtastic import JobtasticTask
import paper_reviewer_matcher as prm

class LinearProgrammingAssignment(JobtasticTask):

    significant_kwargs = [
        ('reviewer_abstracts', str),
        ('article_abstracts', str),
        ('min_rev_art', str),
        ('max_rev_art', str),
        ('min_art_rev', str),
        ('max_art_rev', str),
    ]

    # How long should we give a task before assuming it has failed?
    herd_avoidance_timeout = 5*60  # Shouldn't take more than 60 seconds
    # How long we want to cache results with identical ``significant_kwargs``
    cache_duration = 0  # Cache these results forever. Math is pretty stable.
    # Note: 0 means different things in different cache backends. RTFM for yours.

    def calculate_result(self, reviewer_abstracts, article_abstracts,
                        min_rev_art, max_rev_art, min_art_rev, max_art_rev):
        """
        Generates a csv file with the resulting assignment while it updates the status
        of the process using Celery
        """
        print "lajsldjjdsa"
        update_frequency = 1
        self.update_progress(
                1,
                5,
                update_frequency=update_frequency,
            )
        print "0"
        # this performs the topic modeling (LSA)
        a = prm.compute_affinity(reviewer_abstracts, article_abstracts)
        self.update_progress(
                2,
                5,
                update_frequency=update_frequency,
            )
        v, ne, d = prm.create_lp_matrices(a, min_rev_art, max_rev_art,
                                          min_art_rev, max_art_rev)
        self.update_progress(
                3,
                5,
                update_frequency=update_frequency,
            )
        print "1"
        x = prm.linprog_solve(v, ne, d)
        x = (x > 0.5)
        self.update_progress(
                4,
                5,
                update_frequency=update_frequency,
            )
        print "2"
        b = prm.create_assignment(x, a)
        self.update_progress(
                5,
                5,
                update_frequency=update_frequency,
            )
        print "3"
        return b

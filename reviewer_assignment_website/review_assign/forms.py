from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from crispy_forms.bootstrap import TabHolder, Tab
from django.core.exceptions import ValidationError

from utils import validate_file_extension, generate_pandas_column_validator

class SubmitAssingmentInformation(forms.Form):
    people = forms.FileField(required=True, validators=[validate_file_extension,
                                                        generate_pandas_column_validator(['PersonID', 'FullName'])])
    article_information = forms.FileField(required=True,
                                          validators=[validate_file_extension,
                                                      generate_pandas_column_validator(['PaperID',
                                                                                        'Title',
                                                                                        'Abstract',
                                                                                        'PersonIDList'])])
    reviewers = forms.FileField(required=False, validators=[validate_file_extension,
                                                            generate_pandas_column_validator(['PersonID',
                                                                                              'Abstract'])])
    coi = forms.FileField(required=False, validators=[validate_file_extension,
                                                      generate_pandas_column_validator(['PaperID',
                                                                                        'PersonID'])])
    minimum_reviews_per_article = forms.IntegerField(initial=3, min_value=0, required=True)
    maximum_reviews_per_article = forms.IntegerField(initial=3, min_value=0, required=True)
    minimum_articles_per_reviewer = forms.IntegerField(initial=1, min_value=0, required=True)
    maximum_articles_per_reviewer = forms.IntegerField(initial=20, min_value=0, required=True)

    def __init__(self, *args, **kwargs):
        super(SubmitAssingmentInformation, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'submit-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        # With tabs
        self.helper.layout = Layout(
            TabHolder(
                Tab('Authors and reviewers',
                    HTML('''<div style="padding-bottom:30px;">
                    Upload a <code>.csv</code> file which contains two columns named <code>PersonID</code> and
                    <code>FullName</code>. This file will be used to match <code>PersonID</code> with the articles'
                    authors and reviewer's abstracts and automatically resolve conflict of interests---a reviewer should
                     not review a co-authored article. Download <a href="https://raw.githubusercontent.com/daniel-acuna/reviewer_assignment/master/examples/reviewer_assignment/people_list.csv">
                       example file</a> here.
                     </div>'''),
                    Div('people', title='List of people involved in the review process',
                        css_class="col-xs-offset-4 col-md-offset-4 col-lg-offset-4")
                    )
                ,
                Tab('Articles and reviewers',
                    HTML('''<div style="padding-bottom:30px;">
                    Upload a <code>.csv</code> file with the columns <code>PaperID</code>, <code>Title</code>,
                    <code>Abstract</code>, and <code>PersonIDList</code>. The column <code>PersonIDList</code> contains
                    the list of IDs separated by semi-colon (e.g., <code>1; 5; 34</code>) of the article's co-authors.
                    Download <a href="https://raw.githubusercontent.com/daniel-acuna/reviewer_assignment/master/examples/reviewer_assignment/article_list.csv">
                      example file</a> here.
                    </div>'''),
                    Div('article_information', title='Information about articles'),
                    HTML('''<div style="padding:30px 0;">
                    Upload a <code>.csv</code> file with the columns <code>PersonID</code> and <code>Abstract</code>.
                    You do not always need to specify this file if all reviewers are authors of articles---we will
                    use the article's abstracts to extract the reviewers' abstracts.
                    We will use the articles' abstracts for topic modeling.
                    Download <a href="https://raw.githubusercontent.com/daniel-acuna/reviewer_assignment/master/examples/reviewer_assignment/reviewer_list.csv">
                      example file</a> here.
                    </div>'''),
                    Div('reviewers', title='Information about reviewers')
                ),
                Tab('Conflict of interests',
                    HTML('''<div style="padding-bottom:30px;">
                    Upload a <code>.csv</code> file with the columns <code>PaperID</code> and <code>PersonID</code>
                    indicating which article cannot be reviewed by which person.<br />
                    <em>The system will automatically set co-authors as having conflict of interests</em>

                    </div>'''),
                    Div('coi', title='Conflict of interests',
                        label='Conflicts of interests',
                        css_class="col-xs-offset-4 col-md-offset-4 col-lg-offset-4")
                ),
                Tab('Constraints',
                    HTML('''<div style="padding-bottom:30px;">
                    Set the limits of reviews per article and articles per reviewer
                    </div>'''),
                    Div('minimum_reviews_per_article'),
                    Div('maximum_reviews_per_article'),
                    Div('minimum_articles_per_reviewer'),
                    Div('maximum_articles_per_reviewer')
                ),
            ),
            ButtonHolder(
                Submit('Make assignment', 'Make Assignment',
                       css_class="col-xs-8 col-xs-offset-2 col-md-4 col-md-offset-4 col-lg-4 col-lg-offset-4",
                       style="font-size:22px; margin-bottom:40px;")
            )
        )



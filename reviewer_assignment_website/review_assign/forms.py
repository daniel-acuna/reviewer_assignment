from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit, Div, HTML
from crispy_forms.bootstrap import TabHolder, Tab
from django.core.exceptions import ValidationError

def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv']
    if not ext in valid_extensions:
        raise ValidationError(u'Only CSV files allowed!')

class SubmitAssingmentInformation(forms.Form):
    #paper_information = forms.FileInput(label='paper_information', required=True)
    people = forms.FileField(required=True, validators=[validate_file_extension])
    article_information = forms.FileField(required=True, validators=[validate_file_extension])
    reviewers = forms.FileField(required=False, validators=[validate_file_extension])
    coi = forms.FileField(required=False, validators=[validate_file_extension])
    minimum_reviews_per_article = forms.IntegerField(min_value=0, required=True)
    maximum_reviews_per_article = forms.IntegerField(min_value=0, required=True)
    minimum_articles_per_reviewer = forms.IntegerField(min_value=0, required=True)
    maximum_articles_per_reviewer = forms.IntegerField(min_value=0, required=True)

    def __init__(self, *args, **kwargs):
        super(SubmitAssingmentInformation, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'submit-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''
        # self.helper.layout = Layout(
        #     Fieldset('List of people involved in the process (authors and reviewers)',
        #         HTML('''
        #         PersonID and Fullname <code>.csv</code> file which has two columns contain <code>PersonID, FullName</code>
        #         as shown in example below.
        #         This file will be used to match <code>PersonID</code> with their full name in other files.
        #         '''),
        #         Div('people', title='List of people involved in the review process')
        #     ),
        #     Fieldset('Articles and reviewers',
        #         HTML('''
        #         Papers information <code>.csv</code> file where columns contain
        #         <code>PaperID, Title, Abstract, PersonID list</code>.
        #         Recommended delimiter for the csv file are <code>,</code> or <code>\t</code>.
        #         Example of the csv file is showed below.
        #         '''),
        #         Div('article_information', title='Information about articles'),
        #         HTML('''
        #         Reviewers Abstract <code>.csv</code> which has two columns: <code>PersonID, Abstract</code>.
        #         '''),
        #         Div('reviewers', title='Information about reviewers'),
        #     ),
        #     Fieldset('Conflict of interests',
        #         HTML('''
        #         Pairs of <code>PaperID</code> and <code>PersonID</code> indicating which articles cannot be reviewed
        #         by person ID. The system will automatically set co-authors as having conflict of interests.
        #         '''),
        #         Div('coi', title='Conflict of interests', label='Conflicts of interests')
        #     ),
        #     Fieldset('Constraints',
        #         HTML('''
        #         Set the limits of reviews per article and articles per reviewer
        #         '''),
        #         Div('minimum_reviews_per_article'),
        #         Div('maximum_reviews_per_article'),
        #         Div('minimum_articles_per_reviewer'),
        #         Div('maximum_articles_per_reviewer')
        #
        #     ),
        #     ButtonHolder(
        #         Submit('Make assignment', 'Make assignment')
        #     )
        #
        # )

        # With tabs
        self.helper.layout = Layout(
            TabHolder(
                Tab('Authors and reviewers',
                        HTML('''
                        PersonID and Fullname <code>.csv</code> file which has two columns contain <code>PersonID, FullName</code>
                        as shown in example below.
                        This file will be used to match <code>PersonID</code> with their full name in other files.
                        '''),
                        Div('people', title='List of people involved in the review process')
                    )
                ,
                Tab('Articles and reviewers',
                    HTML('''
                    Papers information <code>.csv</code> file where columns contain
                    <code>PaperID, Title, Abstract, PersonID list</code>.
                    Recommended delimiter for the csv file are <code>,</code> or <code>\t</code>.
                    Example of the csv file is showed below.
                    '''),
                    Div('article_information', title='Information about articles'),
                    HTML('''
                    Reviewers Abstract <code>.csv</code> which has two columns: <code>PersonID, Abstract</code>.
                    You do not always need to specify this file if all reviewers are authors of articles.
                    We will use the articles' abstracts for topic modeling.
                    '''),
                    Div('reviewers', title='Information about reviewers')
                ),
                Tab('Conflict of interests',
                    HTML('''
                    Pairs of <code>PaperID</code> and <code>PersonID</code> indicating which articles cannot be reviewed
                    by person ID. The system will automatically set co-authors as having conflict of interests.
                    '''),
                    Div('coi', title='Conflict of interests', label='Conflicts of interests')
                ),
                Tab('Constraints',
                    HTML('''
                    Set the limits of reviews per article and articles per reviewer
                    '''),
                    Div('minimum_reviews_per_article'),
                    Div('maximum_reviews_per_article'),
                    Div('minimum_articles_per_reviewer'),
                    Div('maximum_articles_per_reviewer')
                ),
            ),
            ButtonHolder(
                Submit('Make assignment', 'Make assignment')
            )
        )

        #self.helper.add_input(Submit('Make assignment', 'Make assignment'))
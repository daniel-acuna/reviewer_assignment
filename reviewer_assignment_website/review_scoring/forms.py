from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, ButtonHolder, Submit, Div, HTML
from django.core.exceptions import ValidationError


def validate_file_extension(value):
    import os
    ext = os.path.splitext(value.name)[1]
    valid_extensions = ['.csv']
    if ext not in valid_extensions:
        raise ValidationError(u'Only CSV files allowed!')


class SubmitScoreInformation(forms.Form):
    scores = forms.FileField(required=True, validators=[validate_file_extension])

    def __init__(self, *args, **kwargs):
        super(SubmitScoreInformation, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_id = 'submit-form'
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.form_method = 'post'
        self.helper.form_action = ''

        # With tabs
        self.helper.layout = Layout(
            HTML('''<div style="padding-bottom:30px;">
                    Upload a <code>.csv</code> file containing <code>PersonID</code>, <code>PaperID</code>,
                    <code>Score</code>, and (optionally) <code>Confidence</code>. The <code>Confidence</code> field
                    indicates how confident the reviewer is giving the score and it should be a positive number in a
                    scale that is shared across reviews.
                    Download <a href="https://raw.githubusercontent.com/daniel-acuna/reviewer_assignment/master/examples/scoring/scores.csv">
                      example file</a> here.
                    </div>'''),
            Div('scores',
                css_class="col-xs-offset-4 col-md-offset-4 col-lg-offset-4"),
            ButtonHolder(
                Submit('Estimate scores', 'Estimate scores',
                       css_class="col-xs-8 col-xs-offset-2 col-md-4 col-md-offset-4 col-lg-4 col-lg-offset-4",
                       style="font-size:22px; margin-bottom:40px;")),
            )

from django.middleware.csrf import get_token
from django.shortcuts import render_to_response
from django.template import RequestContext

from ajaxuploader.views import AjaxFileUploader
from review_assign.forms import SubmitAssingmentInformation
from django.views.generic import FormView
from django.http import HttpResponseRedirect
from django.core.files.base import ContentFile
import django_tables2 as tables
from django.core.urlresolvers import reverse
import pandas as pd

import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings
import uuid


def get_file_path(filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return filename

class index(FormView):
    template_name = 'review_assign/submit.html'
    form_class = SubmitAssingmentInformation

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            # process files, create random names, and save to temporary folder
            people_fn = get_file_path(str(request.FILES['people']))
            # save file
            default_storage.save(os.path.join('tmp', people_fn),
                                ContentFile(request.FILES['people'].read()))
            return HttpResponseRedirect(reverse('result', args=(),
                kwargs={'people_fn': people_fn}))
            # return render_to_response('review_assign/result.html', context_instance=RequestContext(request))
        else:
            return self.form_invalid(form)

class PeopleTable(tables.Table):
    PersonID = tables.Column(verbose_name='ID')
    FullName = tables.Column(verbose_name='Full name')

def result(request, people_fn=''):
    # read file
    path = os.path.join('tmp', people_fn)
    people_data = pd.DataFrame.from_csv(os.path.join(settings.MEDIA_ROOT, path), index_col=None)
    people_table = PeopleTable(people_data.to_dict('records'))
    return render_to_response('review_assign/result.html', {"people": people_table},
                              context_instance = RequestContext(request))



import_uploader = AjaxFileUploader()
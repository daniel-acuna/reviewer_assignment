# Unsupervised reviewer-article assignment based on topic models*

Website that implements the reviewer-article assignment system based on Django, Python web framework.

**This is work-in-progress. Please use at your own risk*

# Members
  - [Daniel Acuna](https://github.com/daniel-acuna) (concept, website, paper writing)
  - [Titipat Achakulvisut](https://github.com/titipata) (website, paper writing)
  - [Tulakan Ruangrong](https://github.com/tupleblog) (website)
  - [Konrad Kording](http://klab.smpp.northwestern.edu/wiki/index.php5/Welcome) (concept, paper writing)

# Requirements
  - [Django 1.7.4](https://www.djangoproject.com/)
  - [Pandas](http://pandas.pydata.org/)
  - [Numpy](http://www.numpy.org/)
  - [Scikit-learn](http://scikit-learn.org/stable/)
  - [gensim](https://radimrehurek.com/gensim/)
  - [unidecode](https://pypi.python.org/pypi/Unidecode)
  - [Django Crispy Forms](http://django-crispy-forms.readthedocs.org/en/latest/)
  - [Django Tables 2](https://django-tables2.readthedocs.org/en/latest/)
  - [Glop (Google's linear programming solver)](https://developers.google.com/optimization/lp/glop)
  - [Celery](http://www.celeryproject.org/)
  - [Django-celery](https://pypi.python.org/pypi/django-celery)
  - [rpy2] (http://rpy.sourceforge.net/)
  - [R] (http://www.r-project.org/) with the [ARM package] (http://cran.r-project.org/web/packages/arm/index.html)

# Installation

We provide `requirements.txt` for all the requirements that we need. After cloning repository, you can do:

```bash
pip install -r requirement.txt
```

In addition of the requirement, we need to install `or-tools` which has installation document on this [link](https://code.google.com/p/or-tools/wiki/AGettingStarted). For Mac OSX, you might find problem installing `or-tools` where we solve that using `easy-install` (see this [issue](https://github.com/daniel-acuna/reviewer_assignment/issues/20))

# Usage

Local usage to launch the website can be created by hovering to where `manage.py` located. Then, you can launch celery worker by running:

```python
celery -A reviewer_assignment_website worker
```

Afterward, you can run the server as follows:

```python
python manage.py runserver
```

# License

*(c) 2014-2015 Daniel Acuna, Titipat Achakulvisut, Tulakan Ruangrong, and Konrad Kording*

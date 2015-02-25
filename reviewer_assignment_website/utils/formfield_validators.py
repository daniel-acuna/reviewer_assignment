
import os
import pandas as pd
import numpy as np

from django.core.exceptions import ValidationError

__all__ = ['validate_file_extension',
           'validate_pandas_columns',
           'generate_pandas_column_validator'
           ]

def validate_file_extension(value, valid_extensions = ['.csv']):
    ext = os.path.splitext(value.name)[1]
    if ext not in valid_extensions:
        raise ValidationError(u'Only CSV files allowed!')

def validate_pandas_columns(value, required_columns = []):
    """Validator generator that the uploaded csv files has the required columns"""
    try:
        df = pd.read_csv(value, index_col=None)
    except:
        raise ValidationError(u'Uploaded file does not seem to be in CSV format')

    # matched columns
    matched = np.array(map(lambda x: x in df.columns, required_columns))
    if not np.all(matched):
        not_matched = np.array(required_columns)[~matched]
        raise ValidationError('The following columns were not found in the CSV file: %s' % ', '.join(not_matched))

def generate_pandas_column_validator(required_columns = []):
    def f(value):
        validate_pandas_columns(value, required_columns)
        value.seek(0)

    return f
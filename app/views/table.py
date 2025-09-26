# Django core libraries
from django.contrib.auth.decorators import login_required
from django.db.models import Subquery, OuterRef
from django.db.models.functions import Substr
from django.shortcuts import render
from datetime import datetime, date
import json

# Application-specific imports
from app.models import *
from .decoratorsCompany import *




from django.shortcuts import render
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _

from erp_framework.reporting.registry import register_report_view
from erp_framework.reporting.views import ReportView

from .models import Expense, ExpenseTransaction


# Create your views here.


@register_report_view
class ExpensesStatement(ReportView):
    report_model = ExpenseTransaction
    base_model = Expense

    report_title = _('Total Balances and detailed statement')

    # group_by = 'expense'
    columns = ['number', 'expense__name', 'date', 'notes', 'value']


@register_report_view
class ExpensesTotalStatement(ReportView):
    report_model = ExpenseTransaction
    base_model = Expense
    report_title = _('Expense Total Balances')
    group_by = 'expense'
    columns = ['name', ('__total__', {'verbose_name': _('Total expenditure')})]

    chart_settings = [
        {
            'data_source': ['__total__'],
            'type': 'pie',
            'title_source': ['name']
        },
        {
            'data_source': ['__total__'],
            'type': 'column',
            'title_source': ['name']
        },

    ]


@register_report_view
class ExpenseMovementTimeComparison(ReportView):
    report_title = _('Expenses Monthly Movements')
    group_by = 'expense'
    base_model = Expense
    time_series_pattern = 'monthly'
    report_model = ExpenseTransaction
    time_series_columns = ['__total__']
    columns = ['name', '__time_series__']

    chart_settings = [
        {
            'id': 'total_movement_bar',
            # 'title': _('Bar - sum'),
            'title': _('Monthly Comparison'),
            'type': 'column',
            'plot_total': 'on',
            'data_source': ['__total__'],
            'title_source': ['name']

        },
        {
            'id': 'total_pie',
            'title': _('Pie - sum'),
            'type': 'pie',
            'data_source': ['__total__'],
            'plot_total': 'on',
        },
        {
            'id': 'balance_bar',
            'title': _('Monthly Comparison By treasury'),
            'data_source': ['__total__'],
            'type': 'column',
            'title_source': ['name']
        },
    ]


@register_report_view
class ExpenseMovementDaily(ReportView):
    base_model = Expense
    report_model = ExpenseTransaction

    report_title = _('Expenses Daily')
    report_slug = 'expenses_daily'
    group_by = 'expense'
    time_series_pattern = 'daily'
    time_series_columns = ['__total__']

    columns = ['name', '__time_series__', '__total__']

    chart_settings = [
        {
            'id': 'total_movement_bar',
            'title': _('Total Expenses Daily'),
            'type': 'column',
            'plot_total': True,
            'data_source': ['__total__'],

        },
        # {
        #     'id': 'total_pie',
        #     'title': _('pie - sum'),
        #     'settings': {
        #         'chart_type': 'pie',
        #         'title': _('total movement comparison by day {expense}'),
        #         'sub_title': '{time_series_pattern} {date_verbose}',
        #         'y_sources': ['__total__'],
        #         'series_names': [_('total movement')],
        #         'plot_total': True
        #     }
        # },
        # {
        #     'id': 'balance_bar',
        #     'title': _('bar - detailed'),
        #     'settings': {
        #         'title': _('treasury expense comparison by day {expense}'),
        #         'sub_title': '{time_series_pattern} {date_verbose}',
        #         'chart_type': 'column',
        #         'y_sources': ['__total__'],
        #         'series_names': ['balance']
        #     }
        # },
    ]

    # @classmethod
    # def get_default_from_date(cls, **kwargs):
    #     import datetime
    #     return now() - datetime.timedelta(days=14) # datetime.datetime(2017,6,1,0,0,)

    @staticmethod
    def get_form_initial():
        import datetime
        return {
            'start_date': now() - datetime.timedelta(days=14),
            'end_date': now()
        }


@register_report_view
class ExpenseMovementDaily2(ReportView):
    base_model = Expense
    report_model = ExpenseTransaction

    report_title = _('Expenses Daily total')
    report_slug = 'expenses_daily_total'
    # group_by = 'type'
    time_series_pattern = 'daily'
    time_series_columns = ['__total__']

    columns = ['__time_series__', '__total__']

    form_settings = {
        'default': True,
        'group_by': 'treasury',
        'aggregate_on': 'expense',
        'group_page_title': _('Expenses Daily Movement'),
        'details_page_title': _('Expense Daily Movement'),

        'time_series_pattern': 'daily',
        'time_series_scope': 'both',
        'group_time_series_display': ['__total__'],
        'time_series_display': ['__total__'],

        'details_columns': ['treasury__slug', 'treasury__title', '__total__'],
        'details_column_order': ['treasury__slug', 'treasury__title', '__time_series__', '__total__'],

        'group_columns': ['slug', 'title', '__total__'],
        'group_column_order': ['treasury__slug', 'treasury__title', '__time_series__', '__total__'],
        'group_column_names': {
            '__total__': _('total expense movement'),
        },

        'time_series_TS_name': _('in'),

        'group_time_series_column_names': {
            '__total__': _('movement'),
        },
    }
    chart_settings = [
        {
            'id': 'total_movement_bar',
            'title': _('Total Expenses Daily'),
            'type': 'column',
            'plot_total': True,
            'data_source': ['__total__'],

        },
        # {
        #     'id': 'total_pie',
        #     'title': _('pie - sum'),
        #     'settings': {
        #         'chart_type': 'pie',
        #         'title': _('total movement comparison by day {expense}'),
        #         'sub_title': '{time_series_pattern} {date_verbose}',
        #         'y_sources': ['__total__'],
        #         'series_names': [_('total movement')],
        #         'plot_total': True
        #     }
        # },
        # {
        #     'id': 'balance_bar',
        #     'title': _('bar - detailed'),
        #     'settings': {
        #         'title': _('treasury expense comparison by day {expense}'),
        #         'sub_title': '{time_series_pattern} {date_verbose}',
        #         'chart_type': 'column',
        #         'y_sources': ['__total__'],
        #         'series_names': ['balance']
        #     }
        # },
    ]

    # @classmethod
    # def get_default_from_date(cls, **kwargs):
    #     import datetime
    #     return now() - datetime.timedelta(days=14) # datetime.datetime(2017,6,1,0,0,)

    @staticmethod
    def get_form_initial():
        import datetime
        return {
            'start_date': now() - datetime.timedelta(days=14),
            'end_date': now()
        }

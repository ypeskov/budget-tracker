from decimal import Decimal
from io import BytesIO

import matplotlib.pyplot as plt
import matplotlib
from fastapi.responses import StreamingResponse
from cachetools import TTLCache, cached
from icecream import ic
from matplotlib.figure import Figure

from app.logger_config import logger

ic.configureOutput(includeContext=True)
cache: TTLCache = TTLCache(maxsize=100, ttl=2)

matplotlib.use('Agg')


def prepare_data(categories, category_id=None):
    """ @category_id - id of the parent category, if None - all top level categories will be used """
    logger.info(f"Preparing data for diagram, for category_id: {category_id}")

    def find_subcategories(cat_id):
        subcategories = []
        for cat in categories:
            if cat['parent_id'] == cat_id or cat['id'] == cat_id:
                cat['name'] = cat['name'].split('>>')[1].strip() if '>>' in cat['name'] else cat['name']
                subcategories.append(cat)

        return subcategories

    parent_categories = [cat for cat in categories if cat['parent_id'] == category_id]
    results = []
    for parent_cat in parent_categories:
        subcategories = find_subcategories(parent_cat['id'])
        total_expenses = sum(cat['total_expenses'] for cat in subcategories)
        results.append({
            'category_id': parent_cat['id'],
            'label': parent_cat['name'],
            'amount': total_expenses,
        })

    return results


def combine_small_categories(aggregated_categories, threshold=0.02):
    """ Combines small categories into one category """
    total_sum = sum(cat['amount'] for cat in aggregated_categories)

    new_other_category = {
        'category_id': 0,
        'label': 'Other',
        'amount': Decimal(0),
    }

    small_categories = []
    for cat in aggregated_categories:
        size = cat['amount'] / total_sum

        if size < threshold:
            new_other_category['amount'] += cat['amount']
            small_categories.append(cat)

    for cat in small_categories:
        aggregated_categories.remove(cat)

    if new_other_category['amount'] > 0:  # type: ignore
        aggregated_categories.append(new_other_category)

    return aggregated_categories


def build_diagram(aggregated_categories, currency_code):
    aggregated_categories = combine_small_categories(aggregated_categories)
    labels = [cat['label'] for cat in aggregated_categories]
    total_sum = sum(cat['amount'] for cat in aggregated_categories)
    sizes = [cat['amount'] / total_sum for cat in aggregated_categories]
    number_of_categories = len(aggregated_categories)
    explode = [0.1] + [0] * (number_of_categories - 1)

    def autopct(pct):
        absolute = int(pct / 100. * float(total_sum))
        return f'{pct:.1f}%\n({absolute:d})'

    fig = Figure()
    ax = fig.subplots()
    ax.pie(sizes,
           explode=explode,
           labels=labels,
           autopct=autopct,
           shadow=False,
           pctdistance=0.8,
           labeldistance=1.1,
           rotatelabels=False,
           startangle=0)

    ax.axis('equal')

    buf = BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)

    plt.close(fig)

    return StreamingResponse(buf, media_type="image/png")

from decimal import Decimal

from app.logger_config import logger


def prepare_data(categories, category_id=None):
    """@category_id - id of the parent category, if None - all top level categories will be used"""
    if category_id is None:
        logger.info("Preparing data for diagram, for all categories")
    else:
        logger.info(f"Preparing data for diagram, for category_id: {category_id}")

    def find_subcategories(cat_id):
        subcategories = []
        for cat in categories:
            if cat['parent_id'] == cat_id or cat['id'] == cat_id:
                cat['name'] = (
                    cat['name'].split('>>')[1].strip()
                    if '>>' in cat['name']
                    else cat['name']
                )
                subcategories.append(cat)

        return subcategories

    parent_categories = [cat for cat in categories if cat['parent_id'] == category_id]
    results = []
    for parent_cat in parent_categories:
        subcategories = find_subcategories(parent_cat['id'])
        total_expenses = sum(cat['total_expenses'] for cat in subcategories)
        results.append(
            {
                'category_id': parent_cat['id'],
                'label': parent_cat['name'],
                'amount': total_expenses,
            }
        )

    return results


def combine_small_categories(aggregated_categories, threshold=0.02):
    """Combines small categories into one category"""
    total_sum = sum(cat['amount'] for cat in aggregated_categories)

    new_other_category = {
        'category_id': 0,
        'label': 'Other',
        'amount': Decimal(0),
    }

    small_categories = []
    if total_sum > 0:
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


# build_diagram function removed - replaced with Chart.js frontend rendering

def register_filters(app):
    @app.template_filter('currency')
    def currency(value):
        try:
            return f"${float(value):,.2f}"
        except (TypeError, ValueError):
            return value

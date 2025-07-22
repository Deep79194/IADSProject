from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.conf import settings
import os


def generate_order_pdf(order):
    template_path = 'emails/order_pdf_template.html'
    context = {'order': order}

    # Render template
    template = get_template(template_path)
    html = template.render(context)

    # Create PDF
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)

    if not pdf.err:
        return result.getvalue()
    return None
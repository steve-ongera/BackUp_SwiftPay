import os
from django_pos.wsgi import *
from django_pos import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO

def link_callback(uri, rel):
    """
    Convert HTML URIs to absolute system paths so xhtml2pdf can access those resources
    """
    # use short variable names
    sUrl = settings.STATIC_URL      # Typically /static/
    sRoot = settings.STATIC_ROOT    # Typically /home/userX/project_static/
    mUrl = settings.MEDIA_URL       # Typically /static/media/
    mRoot = settings.MEDIA_ROOT     # Typically /home/userX/project_static/media/

    # convert URIs to absolute system paths
    if uri.startswith(mUrl):
        path = os.path.join(mRoot, uri.replace(mUrl, ""))
    elif uri.startswith(sUrl):
        path = os.path.join(sRoot, uri.replace(sUrl, ""))
    else:
        return uri  # handle absolute uri (ie: http://some.tld/foo.png)

    # make sure that file exists
    if not os.path.isfile(path):
        raise Exception(
            'media URI must start with %s or %s' % (sUrl, mUrl)
        )
    return path

def print_receipt():
    try:
        # Get template
        template = get_template("sales/receipt_pdf.html")
        context = {"name": "Jorge"}
        html = template.render(context)

        # Create a file to write the PDF to
        with open("receipt.pdf", "wb") as result_file:
            # Create PDF
            pisa_status = pisa.CreatePDF(
                html,                   # the HTML to convert
                dest=result_file,       # the output file
                encoding='utf-8',
                link_callback=link_callback
            )

        # Return True on success and False on errors
        if pisa_status.err:
            print(f"Error creating PDF: {pisa_status.err}")
            return False
        
        print("PDF created successfully!")
        return True

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    print_receipt()
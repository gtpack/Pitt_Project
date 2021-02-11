from django.shortcuts import render
from django.http import HttpResponse
import random
import pandas as pd
import io
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.platypus.tables import Table
from datetime import date
from django.shortcuts import render


def load_page(request):
    return render(request, "simple_sampling.html")


def run_sample(request):
    global samples
    output = io.BytesIO()

    today = date.today()

    val1 = int(request.GET['num1'])
    val2 = int(request.GET['num2'])

    try:
        samples = random.sample(range(1, val1), k=val2)
    except ValueError:
        pass

    # response = HttpResponse(output,content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename="Samples.xlsx'

    df = pd.DataFrame(samples)
    df.columns = ['Sample Item']
    df.sort_values(by=['Sample Item'], inplace=True, ignore_index=True)
    df.index.name = 'Sample Number'
    df.index = df.index + 1
    df['Sample Number'] = df.index
    col_name='Sample Number'
    first_col=df.pop(col_name)
    df.insert(0,col_name,first_col)
    lista = [df.columns[:, ].values.astype(str).tolist()] + df.values.tolist()

    response = HttpResponse(output)
    response['Content-Disposition'] = 'attachment; filename=SamplesReport.pdf'

    elements = []

    header = Paragraph("Auditor Sample Selection")
    population = Paragraph("Population Size: " + str(val1))
    sample = Paragraph("Sample Size: " + str(val2))
    description = Paragraph("This sample was generated using AuditSampling.com. Samples"
                            " generated using this software are generated procedurally using a computer"
                            " aided sampling technique. Samples generated using this method are handled "
                            "by the third-party web service and are free of auditor bias.")
    space = Paragraph(".")
    date_generated = Paragraph("Report Generated on: " + str(today))

    doc = SimpleDocTemplate(response)

    table = Table(lista, colWidths=80, rowHeights=15)

    elements.append(header)
    elements.append(population)
    elements.append(sample)
    elements.append(date_generated)
    elements.append(space)
    elements.append(description)
    elements.append(space)
    elements.append(table)
    doc.build(elements)

    return response



def home(request):

    return render(request,"home.html")

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from numpy import number
from .models import ToDoList,Item
from .forms import CreateNewList,UploadFileForm
import pandas as pd
import openpyxl
from django.conf import settings 
def index(response,id):
    ls = ToDoList.objects.get(id=id)
    if response.method == "POST":
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete == False
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")


    return render(response,"main/list.html",{"ls":ls})

def home(response):
    return render(response,"main/home.html",{})

def create(response):
    if response.method ==  "POST":
        form=CreateNewList(response.POST)

        if form.is_valid():
            n=form.cleaned_data["name"]
            t=ToDoList(name=n)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form=CreateNewList()
    return render(response,"main/create.html",{"form":form})

def practice(response):
    return render(response,"main/practice.html",{})

class ExcelProcessor:
    def __init__(self, number,string_input):
        self.number = number
        self.string_input=string_input
    def process_excel(self, file):
        df = pd.read_excel(file)
        changed_rows = df.copy()
        changed_rows= changed_rows[(changed_rows['Revenue'] <= self.number) & (changed_rows['level1_Name'] == self.string_input)]    
        return df, changed_rows

def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['excel_file']
            number = form.cleaned_data['number']
            string_input = form.cleaned_data['string_input']
            processor = ExcelProcessor(number,string_input)
            df, changed_rows = processor.process_excel(file)
            output_file = 'processed_file.xlsx'
            changed_rows.to_excel(output_file, index=False)
            # with open(output_file, 'rb') as f:
            #     response = HttpResponse(f.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            #     response['Content-Disposition'] = 'attachment; filename=processed_file.xlsx'
            #     return response
            cf_html=changed_rows.to_html(classes="table table-striped")
            df_html = df.to_html(classes="table table-striped")
            return render(request, 'main/excelfile.html', {'df_html': df_html, 'cf_html': cf_html, 'changed_rows':changed_rows,'output_file': output_file})
    else:
        form = UploadFileForm()
    return render(request, 'main/excelfile.html', {'form': form})

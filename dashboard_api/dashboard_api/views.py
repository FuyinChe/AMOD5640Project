from django.shortcuts import render

#404 html
def custom_page_not_found_view(request, exception=None):
    return render(request, "404.html", {}, status=404)

#500 html
def custom_error_view(request, exception=None):
    return render(request, "500.html", {}, status=500)
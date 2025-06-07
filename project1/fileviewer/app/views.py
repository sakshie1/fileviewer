import os
import subprocess
import requests
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse

# Example Google Drive mapping (replace with actual file IDs)
DRIVE_FILE_IDS = {
    "sample1.txt": "1gj0UmhSvklec8eehJbltqHk_LY9W4IRO",
    "sample2.txt": "19a3-f3F-Av-0CyNSNd9erY0LamL1cqt2",
    "sample3.txt": "",
    
}

def index(request):
    filenames = list(DRIVE_FILE_IDS.keys())
    return render(request, 'index.html', {'filenames': filenames})



def view_file(request,filename):
    filename = request.GET.get('filename')
    if not filename:
        return HttpResponse("No filename provided", status=400)

    file_path = os.path.join(settings.BASE_DIR, 'txt_files', filename)
    
    print("DEBUG - Full path to open:", file_path)  # 💡 Add this to confirm the path
    
    if os.path.exists(file_path):
        try:
            subprocess.Popen(['notepad', file_path], shell=True)
            return HttpResponse(f"{filename} opened in Notepad.")
        except Exception as e:
            return HttpResponse(f"Error opening file: {str(e)}", status=500)
    else:
        return HttpResponse(f"{filename} not found locally", status=404)

def download_file(request, filename):
    file_id = DRIVE_FILE_IDS.get(filename)
    if not file_id:
        messages.error(request, 'Invalid file selected.')
        return redirect('index')

    download_url = f'https://drive.google.com/uc?export=download&id={file_id}'
    response = requests.get(download_url)

    if response.status_code == 200:
        file_path = os.path.join(settings.BASE_DIR, 'txt_files', filename)
        with open(file_path, 'wb') as f:
            f.write(response.content)
        messages.success(request, f'{filename} downloaded successfully.')
    else:
        messages.error(request, 'Download failed.')

    return redirect('index')

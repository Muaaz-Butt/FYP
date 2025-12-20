from rest_framework.decorators import api_view
from rest_framework.response import Response
from .tasks import run_application
import threading

@api_view(["POST"])
def submit_application(request):
    mapping_file = request.data.get("mapping_file")

    threading.Thread(
        target=run_application,
        args=(mapping_file,)
    ).start()

    return Response({
        "status": "processing",
        "mapping_file": mapping_file
    })

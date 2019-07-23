from django.http import HttpResponse

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
import logging
from restapi.services.video_service import VideoService
logger = logging.getLogger("Rest")


def index(request):
    return HttpResponse("Hello, world. You're at Leads API.")


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def process_interval(request):
    """
    Store the Result for User Url
    """
    try:
        if request.data.get('video_link', None) is None:
            raise Exception("Url is Required")
        result = VideoService.process_interval(request.data.get('video_link', None),  request.data.get('interval_duration', None))
    except Exception as ex:
        logging.error("Error : ", ex)
        return Response("Could not process" + str(ex), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response(result)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def process_range(request):
    """
    Store the Result for User Url
    """
    try:
        if request.data.get('video_link', None) is None:
            raise Exception("Url is Required")
        result = VideoService.process_ranges(request.data.get('video_link', None),  request.data.get('interval_range', None))
    except Exception as ex:
        logging.error("Error : ", ex)
        return Response("Could not process" + str(ex), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response(result)


@api_view(['POST'])
@renderer_classes((JSONRenderer,))
def process_segments(request):
    """
    Store the Result for User Url
    """
    try:
        if request.data.get('video_link', None) is None:
            raise Exception("Url is Required")
        result = VideoService.process_segments(request.data.get('video_link', None),  request.data.get('no_of_segments', None))
    except Exception as ex:
        logging.error("Error : ", ex)
        return Response("Could not process" + str(ex), status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    return Response(result)
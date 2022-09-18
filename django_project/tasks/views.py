from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from tasks.sentiment_tasks import save_tweets
from celery.result import AsyncResult


def home(request):
    return render(request, "home.html")


@csrf_exempt
def run_task(request):
    if request.POST:
        candidate = request.POST.get("type")
        task = save_tweets.delay(candidate)
        return JsonResponse({"task_id": task.id}, status=202)


@csrf_exempt
def get_status(request, task_id):

    task_result = AsyncResult(task_id)
    result = {
        "task_id": task_id,
        "task_status": task_result.status,
        "task_result": task_result.result
    }
    return JsonResponse(result, status=200)

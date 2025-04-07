#Django imports
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

#Twilio Imports
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client

#Azure imports
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import SystemMessage
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential

#Third parties
import json

def index_view(request):

    return render(request, "main/index.html")

@login_required
def prompt_view(request):

    return render(request, "main/prompt.html")


def dashboard_view(request):
    return render(request, "main/dashboard.html")


def message_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        
        client = Client("SID", "API_TOKEN")

        message = client.messages.create(
            from_="+19704447813",
            body = message,
            to = "+256767623652"
        )

        print(message.body)

    return render(request, "main/dashboard_message.html")


def retrieve_messages_view(request):

    client = Client("SID", "API_TOKEN")
    messages_from = client.messages.list(
        to="+19704447813",
        from_="+256767623652",
    )

    messages_to = client.messages.list(
        to="+256767623652",
        from_="+19704447813",
    )

    messages = [(message.date_sent, message.body, message.from_, message.to) for message in messages_from] + [(message.date_sent, message.body, message.from_, message.to) for message in messages_to]

    messages.sort(key=lambda tup: tup[0])

    return JsonResponse(messages, safe=False)


@csrf_exempt
def model_view(request):
        
    request_body = request.body
    prompt = json.loads(request_body)["message"]
    print(prompt)

    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential("PERSONAL_ACCESS_TOKEN"),
    )

    response = client.complete(
    messages=[
        SystemMessage(""""""),
        UserMessage("In one paragraph" + prompt),
    ],
    model="Llama-3.3-70B-Instruct",
    temperature=0.8,
    max_tokens=1024,
    top_p=0.1
    )

    response_message = response.choices[0].message.content

    return JsonResponse({"response": response_message})


@csrf_exempt
def twilio_automated_response(request):
    resp = MessagingResponse()

    message_body = request.GET.get("Body")

    client = ChatCompletionsClient(
            endpoint="https://models.inference.ai.azure.com",
            credential=AzureKeyCredential("PERSONAL_ACCESS_TOKEN"),
        )

    response = client.complete(
        messages=[
            SystemMessage(""""""),
            UserMessage("In 150  characters," + message_body),
        ],
        model="Llama-3.3-70B-Instruct",
        temperature=0.8,
        max_tokens=1024,
        top_p=0.1
    )

    response_message = response.choices[0].message.content

    resp.message(response_message)
    return HttpResponse(str(resp), content_type='application/xml')


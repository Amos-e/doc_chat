#Django imports
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

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


def prompt_view(request):
    
    return render(request, "main/prompt.html")


def dashboard_view(request):
    return render(request, "main/dashboard.html")


def message_view(request):
    if request.method == "POST":
        message = request.POST.get("message")
        
        client = Client("SID", "API_TOKEN")

        message = client.messages.create(
            from_="TWILIO_NUMBER",
            body = message,
            to = "YOUR_NUMBER"
        )

        print(message.body)

    return render(request, "main/dashboard_message.html")


@csrf_exempt
def model_view(request):
        
    request_body = request.body
    prompt = json.loads(request_body)["message"]
    print(prompt)

    client = ChatCompletionsClient(
        endpoint="https://models.inference.ai.azure.com",
        credential=AzureKeyCredential("GITHUB_PERSONAL_ACCESS_TOKEN"),
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
            credential=AzureKeyCredential("GITHUB_PERSONAL_ACCESS_TOKEN"),
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


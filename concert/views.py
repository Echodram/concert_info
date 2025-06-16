from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InformationSerializer
from .models import Information
import pandas as pd
import logging
from django.http import FileResponse, Http404
import os
from django.conf import settings




class PostInforamtionView(APIView):
    serializer_class = InformationSerializer
    queryset = Information.objects.all()
    def post(self, request):
        nom = request.data.get("nom")
        telephone= request.data.get("telephone")
        recevoir = request.data.get("recevoir")
        
        serializer = InformationSerializer(data = {
            "nom" : nom,
            "telephone" : telephone,
            "recevoir" : recevoir,
        })
            
        if serializer.is_valid():
            info = serializer.save()
            return Response({"id" : info.id },status=status.HTTP_201_CREATED)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

   
def get_file(request):
    if request.method == "GET":
        information = {
            "id" : [],
            "Nom" : [],
            "Telephone" :[],
            "Recevoir les informations" :[],
        }
        try:
            objects = Information.objects.all()
        except Exception as e:
            print(e)
        
        if objects.exists:
            for obj in objects:
                information["id"].append(obj.id)
                information["Nom"].append(obj.nom)
                if obj.recevoirInfo == True:
                    information["Recevoir les informations"].append("Oui")
                else:
                    information["Recevoir les informations"].append("Non")
                information["Telephone"].append(obj.telephone)
                
            file_path = os.path.join(settings.MEDIA_ROOT, "subscriber_for_concert_molded.xlsx")
            df = pd.DataFrame(information)
            df.to_excel(file_path, index=False, engine='openpyxl')
        
            if os.path.exists(file_path):
                response = FileResponse(open(file_path, 'rb'))
                response['Content-Disposition'] = f'attachment; filename="subscriber_for_concert_molded.xlsx'
                return response
        else:
            raise Http404("File does not exist")
    




     
        
               
        
        
        


        
        
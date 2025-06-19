from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import InformationSerializer
from .models import Information
import pandas as pd
import logging
from django.http import FileResponse, Http404
from django.shortcuts import render, HttpResponse
import os
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont



def add_rotated_text_to_image(image_path, output_path, name, ticket_number):
    # Open the original image
    base = Image.open(image_path).convert('RGBA')

    # Create a new blank image with the same size as the original
    txt = Image.new('RGBA', base.size, (255, 255, 255, 0))

    # Initialize ImageDraw
    draw = ImageDraw.Draw(txt)

    # Define font size and type
    font_path = os.path.join(settings.MEDIA_ROOT, 'montserat.ttf')
    font = ImageFont.truetype(font_path, 40)  # Adjust font and size as needed

    # Position for the name
    name_position = (860, 695)  # Adjust based on the image
    # Create a rotated text image for the name
    name_image = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    name_draw = ImageDraw.Draw(name_image)
    name_draw.text((0, 0), name, fill="white", font=font)
    txt.paste(name_image, name_position, name_image)

    # Position for the ticket number
    ticket_position = (220, -5)  # Adjust based on the image
    # Create a rotated text image for the ticket number
    ticket_image = Image.new('RGBA', (300, 300), (255, 255, 255, 0))
    ticket_draw = ImageDraw.Draw(ticket_image)
    ticket_draw.text((0, 0), str(ticket_number), fill="black", font=font)
    ticket_image = ticket_image.rotate(90, expand=1)
    txt.paste(ticket_image, ticket_position, ticket_image)

    # Combine the original image with the text
    combined = Image.alpha_composite(base, txt)
    width, height = combined.size
    scale = 0.5  # Start with 50% size reduction
    img_resized = combined.resize((int(width * scale), int(height * scale)), Image.LANCZOS)
    img_palette = img_resized.convert("P", palette=Image.ADAPTIVE, colors=256)
    
    img_palette.save(output_path, format='PNG', optimize=True)

   
def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        if img.format == 'JPEG':
            img.save(output_path, 'JPEG', quality=quality, optimize=True)
        elif img.format == 'PNG':
            img.save(output_path, 'PNG', optimize=True)
        else:
            img.save(output_path)


class PostInforamtionView(APIView):
    serializer_class = InformationSerializer
    queryset = Information.objects.all()
    def post(self, request):
        host_uri = request.get_host()
        file_path = os.path.join(settings.MEDIA_ROOT, "invitation.png")
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
            download_path = os.path.join(settings.MEDIA_ROOT, f'invitation_sent/invitation_{info.id}.png')
            if info.id <10:
                id = '0' + str(info.id)
                add_rotated_text_to_image(file_path, download_path, nom, id)
            else:
                add_rotated_text_to_image(file_path, download_path, nom, info.id)
                pass
            return Response({"id" : info.id ,
                             "nom" : info.nom,
                             'download_link': f'{host_uri}/invitation/{info.id}'
                             },status=status.HTTP_201_CREATED)
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
                print(obj.recevoirInfo)
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


def download_file(request, id):
    file_path = os.path.join(settings.MEDIA_ROOT, f'invitation_sent/invitation_{id}.png')
    if os.path.exists(file_path):
        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename= invitation_{id}.png'
        return response
    else:
        raise Http404("File does not exist")
        
    


    
    




     
        
               
        
        
        


        
        
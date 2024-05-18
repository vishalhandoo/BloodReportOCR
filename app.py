#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from werkzeug.utils import secure_filename
import os
from wtforms.validators import InputRequired
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import pytesseract
import cv2
import PIL
import pytesseract
import re
import shutil
import pickle
import numpy as np
from sklearn.preprocessing import StandardScaler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'
app.config['UPLOAD_FOLDER'] = 'static/files'
model = pickle.load(open(r'C:\Users\handoo\Downloads\BloodReport\rfc.pkl', 'rb'))
class UploadFileForm(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

standard_to = StandardScaler()
@app.route('/', methods=['GET',"POST"])
@app.route('/home', methods=['GET',"POST"])
def home():
    
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        file_name=file.filename
        print(file_name)
        if file_name.endswith('.jpg'):
            pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract'
            TESSDATA_PREFIX = 'C:\Program Files\Tesseract-OCR'
            img=Image.open(r"C:/Users/handoo/Downloads/BloodReport/static/files/"+file_name)
            text = pytesseract.image_to_string(img.convert('RGB'), lang='eng')
            # print(text_data)
            a = re.search("Name: (\S+)",text)
            name = a[1]
            print("Name:",name) 
            b = re.search("Gender: (\S+)",text)
            gender = b[1]
            if(gender=="Male"):
                gender=1
                print("Gender:",gender)
            else:
                gender=0
                print("Gender:",gender)
            bb = re.search("Age: (\S+)", text)
            Age = bb[1]
            print("Age:",int(Age))
            c = re.search("Hemoglobin: (\S+)",text)
            HGB = c[1]
            print("hemoglobin:",float(HGB))
            d = re.search("Thrombocytes: (\S+)",text) 
            Thrombocytes = d[1] 
            print("Thrombocytes:",float(Thrombocytes))
            e = re.search("leukocytes: (\S+)",text)
            leukocytes = e[1]
            print("leukocytes:",float(leukocytes))
            f = re.search("Neutrophil: (\S+)",text) 
            Neutrophil = f[1]
            print("Neutrophil:",float(Neutrophil))
            g = re.search("Eosinophil: (\S+)",text)
            Eosinophil = g[1]
            print("Eosinophil:",float(Eosinophil))
            h = re.search("Basophil: (\S+)",text)
            Basophil = h[1]
            print("Basophil:",float(Basophil))
            i = re.search("Lymphocyte: (\S+)",text)
            Lymphocyte = i[1]
            print("Lymphocyte:",float(Lymphocyte))
            j = re.search("Monocyte: (\S+)",text)
            Monocyte = j[1]
            print("Monocyte:",float(Monocyte))
            prediction=model.predict([[gender,Age,HGB,Thrombocytes,leukocytes,Neutrophil,Eosinophil,Basophil,Lymphocyte,Monocyte]])
            output=round(prediction[0],2)
            if output<=0:
                return render_template('message.html',message="Enter all values correctly")
            else:
                return render_template(r'clickme.html',name=name,output=output,out={1:[["Perfectly all right"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["No"],["No"],["No"]],2:[["Mild Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["no need to worry,have to take some home remedies and take proper iron rich foods","vitamin B12","vitamin C","Fruits","Iron and Folic","GreenLeafyVegetables"]],3:[["Moderate Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Don't worry it is not a serious issue,take some home remedies","vitamin B-complex","vitamin C","Fruits","Iron and Folic","GreenLeafyVegetables"]],4:[["Severe Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Little serious condition ,don't ignore","vitamin B-complex","Multi-vitamin","Beetroots","red_meat","Iron_rich_food","grains","GreenLeafyVegetables"]],5:[["Dangerous Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Have to consult doctor , it is very dangerous"]],6:[["Mild Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],7:[["Moderate Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],8:[["Severe Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["have to consult doctor","Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],9:[["Basophilia"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Lymphocyte","Monocyte"],["Basophil"],["Feeling weak","Severe Itching","Skin Rashes","Recurring of Infections"],[]],10:[["Eosinophilia"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Eosinophil"],["No specific symptoms"],["Vitamin C","Fruits and Vegetables","Stress free works"]],11:[["Neutrophilia"],["HGB","Thrombocytes","Leukocytes","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Neutrophil"],["Feeling week","Dizy or Faint","Recurrin Unfections","Sores that dont heal"],["Milk Products","Fruits and Vegetables","Meat","Eggs","Fish"]],12:[["Neutropenia"],["HGB","Thrombocytes","Leukocytes","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Neutrophil"],["Fever","Fatigue","Diarrhoea","Mouth Ulcers","Urinary Symptoms"],["Milk Products","Fruits and Vegetables","Meat","Eggs","Fish"]],13:[["Monocytosis"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte"],["Monocyte"],["No specific symptoms"],["Regular Exercise","Reducing Stress","Protect against Infections"]],14:[["Leukocytosis"],["HGB","Thrombocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Leukocytes"],["Fever","Fatigue","Pain","Breathing Difficulty","Rashes"],["Vitamin C","Pappaya","PineApples"]],15:[["Leukopenia"],["HGB","Thrombocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Leukocytes"],["Fever","Mouth Sores","Diarrhoea"],["Avoid Tattoos","Fish","Eggs","Omega3 Fatty Acids"]]})
        elif file_name.endswith('.pdf'):
            images = convert_from_path(r"C:/Users/handoo/Downloads/BloodReport/static/files/"+file_name, 500,poppler_path=r"C:/Program Files/poppler-0.68.0/bin")
            for i in range(len(images)):

            # Save pages as images in the pdf

                images[i].save('page'+ str(i) +'.jpg', 'JPEG')

                src = cv2.imread('page'+ str(i) +'.jpg')

                img1 = cv2.cvtColor(src,cv2.COLOR_BGR2GRAY)

                pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract"

                text = pytesseract.image_to_string(img1)

                # print(text)
                a = re.search("Name: (\S+)",text)
                name = a[1]
                print("Name:",name)
                b = re.search("Gender: (\S+)",text)
                gender = b[1]
                if(gender=="Male"):
                    gender=1
                    print("Gender:",gender)
                else:
                    gender=0
                    print("Gender:",gender)
                bb = re.search("Age: (\S+)", text)
                Age = bb[1]
                print("Age:",int(Age))
                c = re.search("Hemoglobin: (\S+)",text)
                HGB = c[1]
                print("hemoglobin:",float(HGB))
                d = re.search("Thrombocytes: (\S+)",text)
                Thrombocytes = d[1]
                print("Thrombocytes:",float(Thrombocytes))
                e = re.search("leukocytes: (\S+)",text)
                leukocytes = e[1]
                print("leukocytes:",float(leukocytes))
                f = re.search("Neutrophil: (\S+)",text)
                Neutrophil = f[1]
                print("Neutrophil:",float(Neutrophil))
                g = re.search("Eosinophil: (\S+)",text)
                Eosinophil = g[1]
                print("Eosinophil:",float(Eosinophil))
                h = re.search("Basophil: (\S+)",text)
                Basophil = h[1]
                print("Basophil:",float(Basophil))
                i = re.search("Lymphocyte: (\S+)",text)
                Lymphocyte = i[1]
                print("Lymphocyte:",float(Lymphocyte))
                j = re.search("Monocyte: (\S+)",text)
                Monocyte = j[1]
                print("Monocyte:",float(Monocyte))
                prediction = model.predict([[gender,Age,HGB,Thrombocytes,leukocytes,Neutrophil,Eosinophil,Basophil,Lymphocyte,Monocyte]])
                output = round(prediction[0],2)
                if output <= 0:
                    return render_template('message.html', message="Enter all values correctly")
                else:
                    return render_template(r'clickme.html',name=name,output=output,out={1:[["Perfectly all right"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["No"],["No"],["No"]],2:[["Mild Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Week & tired","Pale or yellowish skin","Shortness of breath"],["No need to worry,have to take some home remedies and take proper iron rich foods","vitamin B12","vitamin C","Fruits","Iron and Folic","GreenLeafyVegetables"]],3:[["Moderate Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Don't worry it is not a serious issue,take some home remedies","vitamin B-complex","vitamin C","Fruits","Iron and Folic","GreenLeafyVegetables"]],4:[["Severe Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Little serious condition ,don't ignore","vitamin B-complex","Multi-vitamin","Beetroots","red_meat","Iron_rich_food","grains","GreenLeafyVegetables"]],5:[["Dangerous Anaemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["week&tired","pale or yellowish skin","shortness of breath"],["Have to consult doctor , it is very dangerous"]],6:[["Mild Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],7:[["Moderate Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],8:[["Severe Polycythemia"],["Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["HGB","Thrombocytes","Leukocytes"],["Headache","Fatigue","Dizziness","High BP"],["Have to consult doctor","Fresh Fruits & Vegetables","Whole Grains","Lean Protein"],["Avoid Hill Climbing","Avoid Smoking","Avoid Drinking","Avoid Extreme Temperatures","Avoid Tobacco"]],9:[["Basophilia"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Lymphocyte","Monocyte"],["Basophil"],["Feeling weak","Severe Itching","Skin Rashes","Recurring of Infections"],[]],10:[["Eosinophilia"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Eosinophil"],["No specific symptoms"],["Vitamin C","Fruits and Vegetables","Stress free works"]],11:[["Neutrophilia"],["HGB","Thrombocytes","Leukocytes","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Neutrophil"],["Feeling week","Dizy or Faint","Recurrin Unfections","Sores that dont heal"],["Milk Products","Fruits and Vegetables","Meat","Eggs","Fish"]],12:[["Neutropenia"],["HGB","Thrombocytes","Leukocytes","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Neutrophil"],["Fever","Fatigue","Diarrhoea","Mouth Ulcers","Urinary Symptoms"],["Milk Products","Fruits and Vegetables","Meat","Eggs","Fish"]],13:[["Monocytosis"],["HGB","Thrombocytes","Leukocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte"],["Monocyte"],["No specific symptoms"],["Regular Exercise","Reducing Stress","Protect against Infections"]],14:[["Leukocytosis"],["HGB","Thrombocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Leukocytes"],["Fever","Fatigue","Pain","Breathing Difficulty","Rashes"],["Vitamin C","Pappaya","PineApples"]],15:[["Leukopenia"],["HGB","Thrombocytes","Neutrophil","Eosinophil","Basophil","Lymphocyte","Monocyte"],["Leukocytes"],["Fever","Mouth Sores","Diarrhoea"],["Avoid Tattoos","Fish","Eggs","Omega3 Fatty Acids"]]})
                
        else:
            print("Enter file name correctly")
    return render_template('index.html', form=form)

if __name__ == "__main__":
    app.run(debug=True)


# In[ ]:





# In[ ]:





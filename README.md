# ICMR Project

Structure:
---
>build
>>dataset_build.py

>yolov5
>>requirements.txt

>>train.py

>dataset
- place dataset here


build environments:
---
>install required dependencies:

```
pip3 install -r requirements.txt
```

>run the following command to convert data and label to yolo format:

```
python3 dataset_build.py
```


>train the model: 

```
python3 train.py --data data/carstream.yaml --cfg yolov5s.yaml --weights ''
```

TODO BUG:
---

>utils/dataset.py line 465 to 467
>>I have ignored "duplicate label" error message
>>I have ignored negative values and converted them to their absolute value 

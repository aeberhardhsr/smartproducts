# Smart Products

Smart Products was a module of the specialization in industrial engineering. The aim of the module was to transform a shopping cart into a smart shopping cart. For this purpose an image recognition was created with Yolov3 and Darknet. 

**Pretrained models and config files** are included in smartproducts/NeuralNetwork/..


## Explanation
This script includes motion detection, image recognition, evaluation of the detected images and upload of the data into a database for visualization on a website. 

The script is divided into 5 parts:
1. Part 0: Setting up all the working directories and folders 

2. Part 1: The motion detector takes an initial frame and compares all coming frames with the first one. If there is a deviation of a certain percentage, the motion detector stores the frame in a folder.
3. part 2: The image recognition takes all images from motion detection and tries to recognize the products on the frames. image recognition has been trained with Darknet and Yolov3-Tiny. with OpenCV the .weights and .cfg file is loaded into python and each image is processed individually. If the neural network recognizes a product on an image, the corresponding value is written into a .txt file.
4. Part 3: When all frames have been processed with image recognition, the file 'result.txt' is opened and it is seen which products were recognized on the frames. So that always the best result is written to the database, the file is sorted by the criteria "prediction value". 
5. part 4: The highest prediction value from "result.txt" is taken out and stored in the database. You can be sure, that this product is in your smart shopping cart.

## Installation of prerequisites

### Python modules
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install the python modules.

```bash
pip install opencv-python
```
```bash
pip install numpy
```
```bash
pip install pymysql
```
```bash
pip install tkinter
```

### StartShopping script
For running the script, following changes must be made.

line 159 `label_folder = <YourOwnPath>` Set the path where your file is located.

line 162 `tiny_weights_folder = <YourOwnPath>` Set the path where your file is located.

line 165 `tiny_cfg_folder = <YourOwnPath>` Set the path where your file is located.

line 168 `yolo_weights_folder = <YourOwnPath>` Set the path where your file is located.

line 171 `yolo_cfg_folder = <YourOwnPath>` Set the path where your file is located.

line 174 `mov_dec_folder = <YourOwnPath>` Set the path where you want to store the frames.

line 177 `pro_dec_folder = <YourOwnPath>` Set the path where you want to store the frames.

line 180 `res_dec_folder = <YourOwnPath>` Set the path where you want to store the result.txt file.

line 269 `modelSize = "tiny" ` Default is "tiny" for Yolov3-Tiny, set it to 608 to use Yolov3

line 320 `conn = pymysql.connect('db_host', 'db_user','db_password','database')` Set your own settings



### Webserver
For displaying the data on the website, a webserver with Apache and MySQL is required. I used XAMPP, but you are free in choice. The files for the website are stored in website/
```bash
index.php
cart.png
favico.ico

```
Load the files in the root folder of your webserver. If you want, you can create a subfolder in the root folder.

For your own database settings, change following lines in index.php (use the same as in StartShopping.py line 320)

line 99 `$servername = "db_host";` 

line 100 `$username = "db_user";`

line 101 `$password = "db_password";`

line 102 `$dbname = "database";`

### Database
To store all the data from the products and the predicted images, a databes is required. The database can be set up with the following script stored in db_files/db_layout.sql
```bash
db_layout.sql
```


## Usage

```bash
python StartShopping.py
```

## Workflow
The script starts the webcam and start the movement detector, if a movement is detected a frame will be saved of the detected movement. The movement detector takes 15 frames and then close itself. This 15 frames will be taken automatically by the object detector and processed through the neural network. The neural network detects the products on the frames an give prediction values to the corresponding products on the frames. The results will be saved in a .txt file and then upload into the database. On the website you can see which product was recognized by the object detector.

Movement Detector -> Object Detector -> Analyzing results -> Values to Database -> Visualization on Website

## Contributing
You can download and use the script as you want. If you have any questions, feel free to ask.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)

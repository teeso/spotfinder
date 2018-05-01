# SpotFinder: Connecting people who look for a parking spot with people who have a parking space to share

SpotFinder is a parking solution that connects people who look for a parking spot with people who have a parking space to share. 

The system is powered by a network of modular IoT sensor nodes (that can be placed on streetlight poles). The IoT device consists of a Raspberry-Pi and a camera to capture, and detect free parking spots. Those who want to share parking spot can easily plug the device near to their parking spot, and it will automatically recognize and index when we have a free parking spot. Once it is plugged, those who are looking for a parking spot will find a parking spot easily. 

Think of it as `Airbnb for Parking Spaces`

# Parking Problem in big cities

In urban cities, circling block after block to find an empty parking space is part of the urban driver’s most tedious everyday experience. Hunting for a parking space in a crowded city doesn’t only lead to anxiety, but also increase traffic congestion and pollution [1](http://shoup.bol.ucla.edu/CruisingForParkingAccess.pdf). At the same time, there are thousands of unused parking spaces. Our solutions connects people to ease the traffic.

# Challenges

Designing applications for drivers requires some special considerations. Drivers usually don’t have enough time to deal with complicated and crowded interfaces. Imagine driving down in the street, looking for a place to park in. While driving, you open your phone, look for a map or a mobile application that provides probabilistic estimation on where you can find empty spots, you take some time to open it and start looking on the map for the nearest parking lot. How much time would you spend looking at your phone before making any mistake on the road ? Designing an intuitive UX in these scenarios is essential.

Conversational UIs provides an intuitive solution for drivers. We make use of existing Conversational platforms to bridge the gap between people and machines in urban settings. 


# Social IoT concept

### How can we develop a non-distracting low-cost solution? 

The optimal approach is to re-use existing infrastructure. There is nothing that is geographically organized in big cities as street lamp-posts, lamp-posts have access to power and connectivity and the possibility that they are placed near the parking lots is relatively high. 

What if we make these street light-poles more sociable? What if citizens can talk to light-poles to track and map available parking spots? What if your city can talk back to you whenever you ask where should you park? 

The idea here is to develop a sensor that calculates the number of available spots. Our system takes a form of Social IoT bot, powered by a network of sensors plugged in light poles. The network of sensors capture pictures and upload them to server periodically. Once data is uploaded to the server, the system processes images periodically to count the number of available parking lots, data then would be stored in a centralized database. When a citizen interacts with the system through a chat-bot, the system translates the question to a query, run the query on the centralized database to see what is the nearest parking, and calculate the probability of this person finding an empty spot after the travel time.

The idea behind this overall experiment is to build a network of interactive internet-connected sensors that collect real-time data about the city’s parkings, to tell citizens where to park by calculating the number of available spots and the estimated arrival time. The solution doesn't require installing any app, you just need to interact with this system through Facebook Massenger or Telegram, and the bot will answer you with a parking address and the probability of finding the place empty.


# Solution: SpotFinder 

Creating meaningful experiences when designing smart sensors is not just about plugging a sensor in an interactive network, but also about creating an intuitive experience. In this experiment, we are examining how to make IoT more sociable, to develop a smart sensor that can interact with citizens and help them find parking spots easily.

SpotFinder offers a platform for connected social machines that help people find parking spots, easily. It consists of two components (1) Sensor (2) Server. 


Under the hood, here are the main components at play: 
(1) Image capturing and remote monitoring system
(2) Object detection 
(3) Natural Language understanding 
(4) Spatial indexing 


### Sensor 

The system is powered by a network of modular IoT sensor nodes (that can be placed on streetlight poles). Each IoT node consists of a raspberry-pi and a camera to collect data.

In order to experiment this idea, I used Raspberry Pi and a camera (or you can use Raspberry Pi Camera Shield). This part is intended to showcase the process of developing the concept, so you can develop it yourself.

- Raspberry Pi Model B Revision 2.0 (512MB)
- Raspberry Pi Camera Shield or Logitech HD Webcam C270.
- A usb hub with an external power supply
- WiFi Dongle

![](/docs/prototype/parking_sensor_0.jpg)
**Figure 1** Electronic Componenets of the Sensor

In case you need to set up the Raspberry Pi, which takes less than an hour, follow the [quick start guide](https://www.raspberrypi.org/help/videos/) from the raspberrypi.org site. Adding Wi-Fi connectivity is accomplished by attaching the Wi-Fi dongle and following [the setup guide found on the Raspberry Pi HQ Projects page](http://raspberrypihq.com/how-to-add-wifi-to-the-raspberry-pi/).

I have re-used mounting system for mobile device in order to attach the sensor to the light pole. The sensor is mounted inside Raspberry Pi Camera Case. You can use any box, I used weather proof box for fast prototyping. The reason why I am showing that is to highlight the fact that you don't need fancy things to prototype an idea, You need a powerful device like Raspberry PI, and un-used things laying in your garage.


![](/docs/prototype/parking_sensor_1.jpg)
![](/docs/prototype/parking_sensor_2.jpg)

**Figure 2** Prototype of the Sensor 

![](/docs/prototype/parking_sensor_3.jpg)

**Figure 3** Sensor in parking lot, attached to light-post
Note: If you want to work on fancy case, you can model that and 3D-print it. I don't have access to 3D-printer myself.


Then, we use the sensor to collect data periodically. We use object to detection algorithm on-device to make the solution Private by Design. We don't need to host images in our server, we count the number of cars and send data to the server.


## The system's components

The system consists of three main components: 

1. Data collection component 
    1.1. Collect data from sensors periodically.

2. Data analysis component
    2.1. Question understanding and place identification. 
    2.2. Spatial indexing.
    2.3. Pedictive component to calculate the probability of finding parking spot after time T.

3. Data interaction component
    3.1. Designing and integrating chatbot in social platforms (Facebook Messenger, Telegram, .. etc)


![](/docs/prototype/architechture.png)

## Code Structure

In this project, we have two parts: (1) SpotFinder (Server) (2) SpotFinder (Station)

    +- SpotFinder
    |  +- Server
    |  |  +- Analysis
    |  |  |  +- NLU (Natural Language Understanding)
    |  |  |  +- Spot Detection
    +
    |  +- Station
    |  |  +- Monitor
    |  |  +- Sync
    |  |  +- Analyze

## Sensor Configutation 
- SSH to a connected Raspberry Pi
- Install the required packages `sh install/install.sh`
- Open new screen, so you can keep the script running on the background `Screen -S SpotFinder` 
- Set up a virtual environment
```sh
virtualenv venv 
source venv/bin/activate
```
- Install the required modules using the requirements.txt. `pip install -r requirements.txt`


###  Functionalities: 

- Object detection: Vehicle Counter

At the beginning of the experiment, I tried to use Fast-RCNN, which was initially described in an [arXiv tech report](http://arxiv.org/abs/1506.01497) and was subsequently published in NIPS 2015. The solution was very slow on-device, but it gave good performance on the server. However, I had to capture images using the server, host it on AWS, then apply Fast-RCNN to count the number of vehicles. The solution was not great as it doesn't prioritize people's privacy.

Then, I started using [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/object_detection). By running the wrapper around Tensorflow Object Detection API, we are able to count the number of vehicles. Below is an example of running the script. 

```sh
tf_obj_detector = TFObjDetector(model_name= 'ssd_mobilenet_v1_coco_11_06_2017')
tf_obj_detector.detect_obj(<link_to_image>, viz= True)
```

![](/docs/results/tensorflow_object_detection_api_vehicle_detection.png)
**Figure 3:** Number of Vehicles detected by the model

**Tests**

```sh
python -m src.tests.test_obj_detection
```


## Server Configutation 

In our server, we run three main componenets in a harmony.

###  Functionalities: 

**(1) Natural Language Understanding**

Rasa NLU (Natural Language Understanding) is a tool for intent classification and entity extraction.

- Install RASA NLU `pip install rasa_nlu`
- Rasa NLU rely mainly on MITIE, spaCy or sklearn

The `MITIE <https://github.com/mit-nlp/MITIE>`_ backend is all-inclusive. You can install it via github repo `pip install git+https://github.com/mit-nlp/MITIE.git.`

We need to download the `MITIE models <https://github.com/mit-nlp/MITIE/releases/download/v0.4/MITIE-models-v0.2.tar.bz2>`_ . The file we need is ``total_word_feature_extractor.dat``

- Intall spaCy and sklearn

```sh
pip install -U spacy --user
python -m spacy download en
pip install numpy scipy scikit-learn
```

- Train the model

First, we prepare the training data `parking_rasa.json`. I have put down some examples to train the model (for testing purposes). We need to generate a lot of examples in the next version. Then, we edit `config_spacy.json`, this later hold information on model path and training data.

Start training:
```bash
python -m rasa_nlu.train -c config_spacy.json
```
- Run it on another screen

```bash
python -m rasa_nlu.server -c config_spacy.json --server_model_dir=model_20170717-215842
```

- Test it

```bash
curl -XPOST localhost:5000/parse -d '{"q":"I am looking for a parking spot in khalifa street?"}' | python -mjson.tool
```

The obtained result will look like: 

```bash
{
    "entities": [
        {
            "end": 34,
            "entity": "location",
            "extractor": "ner_crf",
            "processors": [
                "ner_synonyms"
            ],
            "start": 20,
            "value": "Khalifa street"
        }
    ],
    "intent": {
        "confidence": 0.7879162770931989,
        "name": "parking_search"
    },
    "intent_ranking": [
        {
            "confidence": 0.7879162770931989,
            "name": "parking_search"
        },
        {
            "confidence": 0.11158869139329698,
            "name": "goodbye"
        },
        {
            "confidence": 0.07252579527557115,
            "name": "greet"
        },
        {
            "confidence": 0.027969236237933175,
            "name": "affirm"
        }
    ],
    "text": "where can I park in khalifa street"
}

```

Generally speaking, you can see that we are trying to do two things here: (1) identify and classify the user's intention. (2) look for attributes of such queries (a location, a date, etc.). 


- Put the model behind one of the Conversational platforms 

The working version of the bot can be seen in the following screen shot.

![](/docs/results/spotFinder_fb_bot.png)

**Figure 4:** Screen shot of conversational chatbot


## Support

If you are having issues, please let us know or submit a pull request.

## License

The project is licensed under the MIT License.

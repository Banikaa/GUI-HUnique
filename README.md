# GUI-HUnique DEMO GUI application
<h3>-Multi-threaded GUI application for live demo-img multiple Computer Vision models for the HUnique project.-</h3>

<img width="2108" height="947" alt="HUIDEMO_plane1" src="https://github.com/user-attachments/assets/9fb6904f-1393-41a2-807a-eb167feda527" />

<h1>The program allows for live running 5 different models at the same time: </h1>
  - object detection on fingernails, lunulae, knuckles by type (minor, major and base)
  - segmentation of the lunulae
  - tatoo segmentation
  - vein pattern segmentation

The program first allows the user to choose wether they want to test one single foto or with a live feed.

<h3>For a single phot:</h3>
  - the model_manager will start a thread for each model and run them at the same time, displaying each resutls when each thread finishes.
  - the pipeline follows:
      - the FLK model, vein pattern and tatoo model start at the same time on different frames depedning on memory and resources.
      - when the FLK model finishes, 5 threads are started, one for each finger, where the lunulae segmentation model runs on each finger found
  - when a thread is done, it will send back to the specific tab (on top of the screen) and the resutls will be dsiplayed

<h3>For live feed:</h3>
  - the model_manager detects at what tab the user is looking
  - starts a thread only for that model
  - all models are loaded at the begining, so it runs almpost instantly
  - when a user changes the tab, that thread is stopped and another thread with the ohter model is started
  - the images are kept ina separate queue, so if the FPS are slow the image will still run in real time


<h1>Usability features:</h1>
On each tab, the user cam:
  - see sige by side the original image and the image with the segmentation mask overlay
  - zooom in or out in each tab
  - click on each tab to make it occupy the full width of the screen
  - change the color/ thickness of the masks
  - seemlelsy change between the models and tabs, and between live feed and single photo modes
  
  

<b>Note:</b> due to GDPR constraints, the models weights and the images captured during the demo sessions cannot be shown.

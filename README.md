
# Smart Vehicle Detection for Toll-Gates
 
<p align="center">
  <img src="https://user-images.githubusercontent.com/77114909/191062454-61c068c5-2204-41eb-a875-3db1d4c81eba.png" />
</p>

============================================================================================


# Application Overview
In  our toll gate systems, each vehicle would be required to 
stop at the entrance to acquire permission to proceed and also stop at the exit to pay the bills.
This would lead to a possible congestion (traffic)  and a delay in time at these two instances.
This project proposes an efficient solution to this problem.

In this project, two cameras will be positioned both at the entrance and exit. The camera at the entrance would be used to identify the vehicles while the same vehicles would be re-identified using the camera positioned at the exit.

Due to this, the need to stop would be only on one occastion. Thus, the traffic  and the waiting time could be minimised.

The classification of the vehicles would be performed primarily focusing only on their appearences, setting aside the detection using number plate recognition approach.

![vivotek-IB9387-LPR-4__09325 1562171672](https://user-images.githubusercontent.com/77114909/190961760-4cf5beaf-dc0b-442d-87f1-0771866d141d.jpg)![0_Speed-cameras-on-motorway](https://user-images.githubusercontent.com/77114909/190962672-816c5c12-14a1-4348-8bac-f7bde3151c09.jpg)

## Related Works

* [Image processing based vehicle detection and tracking method](https://ieeexplore.ieee.org/document/6868357)<br>
  P. K. Bhaskar and S. -P. Yong, "Image processing based vehicle detection and tracking method," 2014 International Conference on Computer and Information Sciences (ICCOINS), 2014, pp. 1-5, doi: 10.1109/ICCOINS.2014.6868357.
  
* [vehicle detection and counting system](https://rdcu.be/cVSWT)<br>
  Song, H., Liang, H., Li, H. et al. Vision-based vehicle detection and counting system using deep learning in highway scenes. Eur. Transp. Res. Rev. 11, 51 (2019). https://doi.org/10.1186/s12544-019-0390-4
 
* [Car Reidentification System using Image Processing](https://www.researchgate.net/publication/258222322_Car_Reidentification_System_using_Image_Processing)<br>
  Bligny, Timothee. (2013). Car Reidentification System using Image Processing. 

* [Vehicle Detection Based on Color and Edge Information](https://www.researchgate.net/publication/221472002_Vehicle_Detection_Based_on_Color_and_Edge_Information)<br>
  Gao, Lei & Li, Chao & Fang, Ting & Xiong, Zhang. (2008). Vehicle Detection Based on Color and Edge Information. 142-150. 10.1007/978-3-540-69812-8_14.  



## Support

<a href="https://www.buymeacoffee.com/5Zn8Xh3l9" target="_blank"><img src="https://www.buymeacoffee.com/assets/img/custom_images/purple_img.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

<p>Or</p> 

<a href="https://www.patreon.com/amitmerchant">
	<img src="https://c5.patreon.com/external/logo/become_a_patron_button@2x.png" width="160">
</a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS
## Project Plan
* It should be noted that there may be unforeseen delays and changes to the original plan, making the following plan rather optimistic.

![Screenshot 2022-09-19 204420](https://user-images.githubusercontent.com/77114909/191054486-7ba7b810-9345-4220-a29f-4ff9f2c23303.jpg)

## Process
![Screenshot 2022-09-19 122416](https://user-images.githubusercontent.com/77114909/190963962-f4e19ca4-7dec-4b54-9f59-79ab4b68b864.jpg)

## Tools
* Cameras
* Micro Controllers
## Visualization
* Visualization of the data from the database using React

![Screenshot 2022-09-19 212441](https://user-images.githubusercontent.com/77114909/191060384-34bd1299-b034-4346-a610-31185e7da523.jpg)

## Feedback
* The Feedbacks from Project Evaluators

| Identified Problems    | Solutions     | 
| ---------------------- | ------------- | 
| Different quality of image if different Cameras are used.| Use the same camera with the same type of white balance, same quality, same lens       | 
| The entrance cameras detect at evening and exit cameras detect at night                  | Detection of vehicle considering the lightintensity of the surrounding
| Difference in the speed of the vehicle at entrance and exit    | build speed barrier system at the video capturing point of both entrances    | 
| Difficulty in obtaining datasets for all 5 or more <br> specifications like color, dimension, model, <br> vehicle type, defects, other unique <br> characteristics. Thus, difficulty in classification of the vehicles.    |Reduction of specifications. <br> Focus on the more important ones only      |

# Alz.vision

## Inspiration
Nearly 3 million people in the US alone fall victim to memory impairments such as dementia and Alzheimer's. Currently, when doctors diagnose patients, they don't personally know the person and have never met them before. They rely on mental tests and interviewing the family members. They don't have any real, concrete historical data their memories or any data on their decline of their memory. We hope to provide a data-analysis tool for doctors to better get an idea of each patient.

## What it does
Our web application hopes to provide doctors with data on users to help them better diagnose Alzheimer's. The user uploads photos and videos to the application, along with a description of the event portrayed. As the user continues to upload photos and videos, they will be prompted to recall the memories by writing another description. Our deep neural network algorithm will analyze the two descriptions to determine their similarity. Using the data obtained, the app provides graphs and visual aids to show a user's memory decline. In addition, it will search for any potential outliers in their memory loss and common keywords associated with those outliers. Overall, the app provides data to a user on the rate at which their memory is declining and keywords associated with their decline, offering concrete, reliable data for both doctors and patients.<br>
By analyzing and performing data analytics on the user’s memory over time, Alz.vision is able to use state of the art machine learning algorithms to detect powerful trends as well as create compelling and easy to understand graphs, helping users take a more active role in their health and helping doctors make a better and more informed Alzheimer’s and dementia diagnosis. With more testing of our algorithm, we plan to expand our application to warn users if their declination of memory suggests Alzheimer’s or dementia and recommend that the user visits a doctor.


## Accomplishments that we're proud of
We finally got the app together! We were really proud of how our application is currently more or less functional. We can successfully upload memories and display them for redescribing. Also, our machine learning analysis is integrated into our app, so we're really happy about how everything is coming together. We should be ready to pitch our app and put it out to production. 

## How we built it
We used Flask only for this MVP, and we redesigned our original website. We used Flask-Mongodb instead of Mongodb and we used MongoDB Atlas. For the frontend, we used HTML/CSS/JS with Bootstrap. We used the same machine learning algorithms from our last sprint. 

We built our app with a mobile app and a basic website for the front end, a Flask API to allow us to access the machine learning models, and a MongoDB Atlas for the backend. We built the app using React Native, and we built the website using HTML/CSS/JS and Flask. For the machine learning in the analysis, we used StringMatcher and SequenceMatcher to rate each sentence and regressions and Isolation Forest to find outliers, and the charts were made using matplotlib.pyplot. Then, we used MongoDB Atlas to store each user's memories and descriptions that our front ends could use. 

## Challenges we ran into and What we learned
It was particularly difficult for us to upload images through MongoDB and we learned a lot about images with MongoDB and that there was a library which handled MongoDB with Flask (we were originally using only the original MongoDB library).

For both the outlier detection and the sentence similarity scores, we tested a few models before reaching our final decision on the model which worked best. It was our first time using MongoDB Atlas and mongod, so it took some time to learn about the API. It was also a little difficult to work together online, but we used Discord as our platform and was sure to periodically check-in on each other.

First, from a non-technical standpoint, our team learned a lot about Alzheimer's. We spent two weeks researching the disease to learn more about how it is diagnose and listening to real user stories. From a technical standpoint, all our teammates learned MongoDB Atlas and worked much more with Flask. 

## Next Steps
We hope to share our app with local doctors to get their feedback on our app. We will adjust accordingly and then continue the design process to create a finished product. We especially want their feedback on how to display the data which will be most convenient to them. Then, we will pitch this product to local hospitals and clinics and hopefully collaborate with them to make this product a tool for patients to collect data to help doctors to diagnose dementia and Alzheimer's better. Overall, we hope to push this out to _help_ the world, and we hope to make adjustments to the app to help the world.

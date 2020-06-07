# Alz.vision

## Inspiration
Nearly 50 million people worldwide fall victim to memory impairments such as dementia. We personally have met people who struggle with Alzheimer's and have forgotten critical information and cherished memories, even going as far as forgetting a loved one. And according to a report from Alzheimers Disease International, nearly 75% of Alzheimers patients worldwide go undiagnosed. Currently, when doctors diagnose dementia, they lack concrete data on a patient’s decline of memory, relying on a combination of brain scans, memory tests, and interviews with family members.

## What it does
We decided to create Alz.vision, a web application that uses machine learning to help potential Alzheimers and Dementia patients. The app has 3 core components.
1. First, it prompts users to upload memories each day with a single sentence describing the memory.
2. Second, as time passes, the app prompts users to describe memories they have uploaded in the past again. Each of these descriptions are analyzed by a Siamese LSTM deep neural network and are assigned scores.
3. Using state-of-the-art machine learning algorithms, such as Random Forest regression, Support Vector Regression, and clustering to name a few, the app analyses the scores and displays compelling graphs and statistics in real time for users and their doctors to view

By using machine learning to analyze many memories over time, Alz.vision is a data analysis tool that analyzes a user’s memory for signs of memory loss and provides doctors with key data to make a more accurate and informed diagnosis. The user uploads photos and videos to the application, along with a description of the event portrayed. As the user continues to upload photos and videos, they will be prompted to recall the memories by writing another description. Our Siamese LSTM deep neural network algorithm will analyze the two descriptions to determine their similarity. Using this data and algorithms such as Random forest regressions, Support vector regressions, Linear Regressions, and Natural Language Processing, the app provides graphs and visual aids to show a user's memory decline. In addition, it will search for any potential outliers in their memory loss and common keywords associated with those outliers. 

Overall, by analyzing and performing data analytics on the user’s memory over time, Alz.vision is able to use state of the art machine learning algorithms to detect powerful trends as well as create compelling and easy to understand graphs, helping users take a more active role in their health and helping doctors make a better and more informed Alzheimer’s and dementia diagnosis. With more testing of our algorithm, we plan to expand our application to warn users if their declination of memory suggests Alzheimer’s or dementia and recommend that the user visits a doctor.


## Accomplishments that we're proud of
We got the entire web application working together! We were really proud of how our application is currently functional and accurately creating graphs in response to user descriptions in real time. We can successfully upload memories and display them for redescribing. Also, our machine learning analysis is integrated into our app, so we're really happy about how everything is coming together. We should be ready to pitch our app and put it out to production. 

## How we built it
We used Flask, HTML, CSS, JS, and Bootstrap for the frontend and backend for this project. We used Flask-Mongodb and MongoDB Atlas as our database to store user information, images, descriptions, and scores. For the frontend, we used HTML/CSS/JS with Bootstrap. We implemented a Siamese LSTM Deep neural network, Linear regressions, Random Forest regressions, Support Vector Regressions, and Natural Language Processing to analyze the descriptions and create compelling and meaningful graphs for both patients and doctors.


## Challenges we ran into and What we learned
It was particularly difficult for us to upload images through MongoDB and we learned a lot about images with MongoDB and that there was a library which handled MongoDB with Flask (we were originally using only the original MongoDB library). It was also difficult for us to figure out how to return images from our machine learning algorithms to display on the website. We finally learned how to convert the graphs to base64 images, which we could then display on the website using HMTL.

For both the outlier detection and the sentence similarity scores, we tested a few models before reaching our final decision on the model which worked best. It was our first time using MongoDB Atlas and mongoDB, so it took some time to learn about the API. It was also a little difficult to work together online, but we used Discord as our platform and made sure to periodically check-in on each other.

From a non-technical standpoint, our team also learned a lot about Alzheimer's. We spent two weeks researching the disease to learn more about how it is diagnose and listening to real user stories.


## Business Model
### Market
According to WHO, There are nearly 10 million new cases of Dementia per year worldwide approximately, furthermore according to Alzheimers disease international 75% of people with dementia have not received a diagnosis. This makes our total market size over 40 million people.

### Revenue Model
In terms of our revenue model, we will choose to make revenue in 2 key ways: Advertisements, and by offering a premium subscription offering advanced data analytic features and providing greater insight into a user’s change in memory.

### Competitive Advantage
Finally, the competitive advantage. Current methods of diagnosing Alzheimers and Dementia include Interviewing family members, and conducting memory tests and brain scans, but there is no concrete data. Alz.vision on the other hand, analyzes images and memories over time to measure the change in memory, Uses ML and neural network to detect trends and patterns, and most important, provides concrete data.

## Next Steps
We hope to share our app with local doctors to get their feedback on our app. We will adjust accordingly and then continue the design process to create a finished product. We especially want their feedback on how to display the data which will be most convenient to them. Then, we will pitch this product to local hospitals and clinics and hopefully collaborate with them to make this product a tool for patients to collect data to help doctors to diagnose dementia and Alzheimer's better. Overall, we hope to push this out to _help_ the world, and we hope to make adjustments to the app to help the world.
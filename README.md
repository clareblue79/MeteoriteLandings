# MeteoriteLandings
## Wellesley CS349 Distributed Computing Final Project 

**By Chetna Mahajan and Clare Lee**

Check out the Data Visualization Demo: https://youtu.be/IgL1I5NOKfI

### Introduction
We conducted exploratory data analysis and visualization of the NASA documented meteorite landings using Amazon’s EMR with Hadoop, mrjob (a Python module for Hadoop), and D3.js. 

We wanted to explore using the PAAS model of cloud computing as it is one of the most commonly used models in industry, specifically given all the platforms and services AWS provides now. We wanted to see how user-friendly and beginner-friendly Amazon’s EMR service is since it is a well-known service that allows users (individuals or small-, mid-, and large-sized companies) to have access to a Hadoop cluster for a fee without having to use resources and manpower to set up said cluster that they can scale up and down as they need. We also wanted to think more about the usefulness of Hadoop and MapReduce in the context of exploratory data analysis for data visualization -- we decided the best way to do this would be to apply Hadoop’s MapReduce to explore a dataset and then evaluate whether there was a better way to do this.

We approached using Amazon EMR from the perspective of someone working with data -- say a multipurpose data scientist -- who is a beginner to Hadoop (and/or to the industry!). Our process for this project mimicked the process of someone conducting data analysis in the real world; we cleaned the data and filled missing parts of the data, then we conducted a list of exploratory analyses of interest (based on frequency, time -- descriptive statistics), and then we visualized the data in order to get a better understanding of the dataset. The scope of our project ended at visualizing the exploratory data analyses, but given more time, this is a process that would lead to us drawing questions and conclusions from the dataset (such as, country x has a large volume of meteorite landings -- is that because it gets more meteorites or is it because the space program in this country gets significant funding and so it tracks their meteorite landings better?).

Interweaved with the data analysis process was our process of navigating Amazon’s EMR service, specifically for Hadoop’s MapReduce. This involved a lot of digging around to read documentation, old tutorials, new tutorials, StackOverflow explanations, debugging attempts, etc. Finding the right tool to use with Amazon’s EMR took a while and was a very frustrating process to go through. However, it was also a very good learning experience for us in terms of making applications in the real world, where good documentation is highly valuable but might not be available for every platform or service we want to use, so learning how to navigate that and find something that did work and meet our project’s needs was very helpful.

The following is a report on our project, including the process, implementation details about the various aspects of our project, the results of our data analysis, and a reflection on the whole process of using PAAS, evaluating Amazon’s EMR, and evaluating Hadoop in the context of our dataset and our data analyses.

### Implementation Details
#### Dataset and Updating the Data
As described in our Phase 2 report, we used a dataset of documented meteorite landings made public by NASA. This dataset contains 45,000+ rows, with each row representing a unique meteorite landing. The dataset provides the following characteristic of each meteorite: name, ID, type, mass, year landed/found, and geolocation (longitude, latitude). 

The dataset isn’t a perfect one. Some entries don’t have a value for a given characteristic. Some entries have valid values but according to their geolocation are in a place not mappable to a country (i.e. in a body of water). Some entries have an additional column. We had to decide when to take care of each of these things.

In our data cleaning and updating phase, we mapped every entry’s geolocation to a country using Google Map’s API and geocoder (a python module that allows access to Google Map’s API without a key!). We did not end up using Amazon EMR for the data cleaning phase because every time we put the code for our data cleaning phase into Amazon EMR, it returned a failed step. Since we were worried about the time it would take us to do data analysis and data visualization after we figured out how to get a working solution with Amazon EMR, we decided to launch multiple EC2 instances on AWS (to get around the 2500 requests per day per IP) and split up the dataset into smaller chunks and combine the output into a cleaned, updated dataset. This “new” dataset now had a country characteristic for every entry -- or a None if no country was identifiable.

A note on this updated dataset: we found that an enormously large number of entries were mapped to Antarctica or country ‘None’. This is of course extremely concerning. The large volume of meteorites mapped to Antarctica is explainable by the fact that a large volume of all found meteorites are found in Antarctica. The large volume of ‘Nones’ though are definitely concerning -- we are unsure of why precisely this happened. Some of those are geolocations mapped to bodies of water, so it makes sense that they aren’t associated with a country. Others are on borders between countries, so perhaps that makes sense as well. But, there are entries with valid geolocations that were mapped to None by GoogleMaps’ API. We are not sure what the reason for this is. We do know that the mapping error is not a result of the limits to the API, as we checked each output file for the updated dataset and it was not the case that once we found one entry mapped to ‘None’, every subsequent entry was also marked as ‘None’, which would suggest that the API request limits had been reached. Since we did not exclude any entry, any entries mapped to ‘None’ are still valid entries in the decade frequency and decade mass analyses, as long as the entry had some input for decade and mass. While this didn’t solve the problem of the mapped to ‘None’ entries, it does make sure that a weakness in one analysis does not affect another, unrelated analysis.

#### Navigating Amazon EMR

As we mentioned in the introduction, this was the most frustrating aspect of the whole project. Considering how popular AWS is and how much business Amazon has gotten through its PAAS software, we expected there to be a large amount of helpful documentation from Amazon and other sources on using Amazon EMR with Hadoop. One problem was that most tutorials we found that worked with Java were 4+ years old. Another problem was the amount of setup involved with Java -- some tutorials recommended using Eclipse IDE, others said we needed to have Maven installed so we could build dependencies, etc. 

While trying to navigate through using Amazon EMR with Hadoop, we found the Hadoop Streaming option -- which lets you write the mapper and reducer in Python, does not involve importing Hadoop, and in general, abstracts over the details of Hadoop so that the user only has to think about the mapper function and the reducer function. Amazon’s EMR does the heavy lifting of configuring Hadoop in the backend. This seemed like the best option for our data analysis needs -- and that too with clean, concise Python code.

Unfortunately, despite meticulously following tutorials (both Amazon-provided and external), each of our attempts (steps, as they’re called in a cluster) failed. We are not sure why this happened -- we checked the log files, but the errors are rather general and all our debugging searches were not fruitful.

Finally, after hours and hours of not finding a working solution with Hadoop Streaming, we found mrjob, a Python module that makes working with Hadoop and Amazon EMR extremely easy and quick. With mrjob, you can test your code locally before testing it with EMR to make sure no syntactical errors exist before you use up resources. Another benefit of mrjob is that you see a local run of your code and a run on EMR or Hadoop in the same way -- all output is printed to command line as well as relevant error messages, if errors come up. Detail on how to use mrjob with Amazon EMR can be found in the tutorial.

In the end, we were able to use mrjob to use Amazon EMR with Hadoop. Like Hadoop Streaming, mrjob also abstracts over all the details of Hadoop that are not necessary for simple map and reduce functions -- which made it perfect for our purposes. If we had needed direct access to Hadoop’s API, mrjob would not have been the best solution -- using Java with Hadoop would have been the best solution.

### Results
The results of our data analyses conducted using map-reduce provide some interesting insights into the dataset. For example, Antarctica has 11756 meteorite landings in the dataset. Namibia only has 9 landings in the dataset, but has the highest total mass of all meteorites (>60 million grams) -- this is definitely something that should be looked into further as it could reveal an error in the dataset or something about the meteorites found in Namibia. The decade 2000 has the greatest number of meteorites (17,756), but the decade 1920 has the greatest total mass (>72 million grams) even though only 159 meteorites have landed in 1920. This could reveal an error in the dataset, or perhaps the mass of a lot of meteorites that landed in 2000 was not recorded since the total mass only represents entries for which a mass was entered.

### Evaluation of Technolgies Used
#### Amazon EMR
We expected this to be a lot more beginner-friendly and were surprised to discover it wasn’t. However, in that discovery, we did find a tool that is not only beginner-friendly but also the best tool to use for simple map-reduce jobs since it separates the Hadoop details from the map-reduce details. The best solution for anyone who needs to use Hadoop and MapReduce for a simple task (and simply needs to use the Hadoop cluster but does not need a great deal of access to Hadoop’s API), mrjob is the best tool. Hadoop Streaming that Amazon EMR has functionality built in for would come a close second, but since we weren’t able to get that working, we can’t recommend it. Mrjob also has the best documentation (in existence anywhere, potentially), which is a great deal of help to beginners for a quick start.

#### Hadoop in the context of this dataset
Through this project, we wanted to see how Hadoop could be used in exploratory data analysis. We know Hadoop is not ideal for real time data analyses or anything that requires too much time from the mapper or reducer (in fact, Amazon’s EMR cluster has a timeout for how long a mapper or reducer is allowed to run before EMR declares something is wrong and fails -- the timeout variable is changeable). We know that Hadoop’s MapReduce is best used for batch processing. We have learned from this project that while Hadoop’s MapReduce was useful for our dataset, it was probably a waste of resources considering one computer can process our whole dataset. We did not notice any difference between the time it took Hadoop and EMR to conduct a step and the time it took that step to run locally (using mrjob) -- in fact, Hadoop and EMR took longer and used more computers because creating a cluster takes around 7-8 minutes. We also saw from this project how Hadoop’s MapReduce would be very useful and perhaps even necessary in conducting exploratory data analysis on a dataset (much) bigger than ours but similar in nature.


### Future work
#### Data analysis
Future analyses that could be conducted based on this dataset and the analyses we have already conducted include figuring out if certain points are erroneous or if there’s a story behind them -- are Namibia’s meteorites really that much heavier or is it an error? Another consideration for future work would be to figure out a more accurate mapping for some of the erroneous ‘None’s in the geolocation to country mapping.

#### Amazon EMR + Hadoop
With more time, we would be able to delve into the intricacies of Java and Hadoop and discover why a greater amount of access to Hadoop’s API might be useful. It would also be interesting to use Spark instead of Hadoop and conduct both exploratory data analyses as well as regressions and causal analyses. With more time, it would also be interesting to do a multistep map-reduce job, either with mrjobs or Hadoop Streaming or Java!

### Summary
Our project had two main aspects to it: navigating Amazon EMR with Hadoop and data analysis/visualization. Overall, this project gave us a chance to explore the usability of a popular PAAS (Amazon EMR) from a beginner’s perspective and apply what we learned about Hadoop in class to a dataset to evaluate whether Hadoop should be used in every case (especially a case where the dataset is *relatively* small).


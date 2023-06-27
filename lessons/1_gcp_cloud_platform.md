# Cloud Platforms

## What are cloud platforms and why use them?
Imagine you write a python program which should run once a day and make some data transformations. What do you need before getting started?
1) Hardware: You need a computer where you can install and run your python program
2) Software: You need to install a new version of Python on your computer. Also install other libraries like pandas, requests and so on.
3) Maintaing: You need to make sure your hardware doesnt break and your software is always updated.

Now Cloud Platforms can help us with all of those 3 components. 
Cloud Platforms have big computing and data centers. There have basically thousends of computers ready to work.
![image](assets/cloud_server.png)

So now imagine instead of running your python program on your computer you let it run on a computer on a cloud computer. What are the benefits?
1) Your computer could break, get stolen. A cloud computer is save from damage.
2) Your computer GPU and memmory is limited. If you have a complicated program which needs a lot of ressources, your computer might be not good enough.
3) Coud platforms also manage software for you. They can give you access to a computer which already has installed everything you need.
4) If the software need updates, they take care of it.

So basically, you can outsource hardware and software infrastructure almost completely. The only thing you need is a internet connection to access it.

## Companies using cloud platflorms
Of course for a single person, with a single python program there is no necessity to use a cloud platform.
But now imagine you are a big company with many databases, programs, AI models. You need to buy all the computers and put them in your office, or somewhere. Then you need an IT department which makes everything work, installs and maintains all the software. Those are a lot of fix costs and a big initial investment. Also its not very scalable. If you suddenly need much more or much less ressources you are not very flexible to adjust.


Here is a good video which explains the benefit of using cloud services instead of on premise solutions:
https://www.youtube.com/watch?v=1ERdeg8Sfv4


## Cloud Platform Provider

Now you know what the general concept of a cloud platform is. There are endless different cloud platforms. But there is a handful of big and most popluar cloud platforms
1) AWS
2) GCP
3) Azure
4) IBM

All of them offer basically very similiar services. But all of them have some benefits. While AWS is the most used platform, GCP is more user and beginner friendly and the best way to get started.


## GCP (Google Cloud Platform)

So, we are going to work with GCP.
GCP has different services which offer you to some degree hardware, software and maintanance and an easy interface.

Some important solutions for a data engineer:
1) Storage: A service to store files.
2) Big Query: A scalable database for BIG Data
3) Composer: A service which helps you to schedule your ETL tasks (Airflow).
# Threatter

A social networksite inspired by Meta's 'threads'.

Website Link : https://threatter.site/

## Table of Contents

- [Introduction](#introduction)
- [System Architecture](#system-architecture)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Usage](#usage)
- [Table Schema](#table-schema)
- [API Documentation](#api-documentation)
- [Contact](#contact)

## Introduction

The project is a social platform supporting post creation, comment replies, and following users. It addresses the need for content filtering and recommendation by providing personalized post suggestions as well as popular post recommendations. Additionally, the platform includes a real-time notification system to keep users updated on interactions promptly.

## System Architecture
<img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/%E5%B0%88%E6%A1%88%E5%BE%8C%E7%AB%AF%E6%B5%81%E7%A8%8B%204%20.png" alt="System Architecture" width="800"/>

## Features

- User Management: Supports user registration, login, and profile management
- Personalized Post Recommendations: Recommendation system based on user's follows
- Popular Post Recommendations: Highlights popular content based on interaction data
- Real-Time Notifications: Pushes interaction updates to users using real-time streaming (Sever-Sent-Events)

## Tech Stack

| **Category**    | **Technology**                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| **Backend**     | ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi&logoColor=white) ![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **Frontend**    | ![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black) ![HTML](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white) ![CSS](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)                                                                                                                                                                                                                                                                                                                                              |
| **Database**    | ![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white) ![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat&logo=redis&logoColor=white)                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **DevOps**      | ![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat&logo=docker&logoColor=white) ![AWS S3](https://img.shields.io/badge/AWS%20S3-569A31?style=flat&logo=amazonaws&logoColor=white) ![AWS EC2](https://img.shields.io/badge/AWS%20EC2-FF9900?style=flat&logo=amazon-ec2&logoColor=white) ![AWS Route53](https://img.shields.io/badge/AWS%20Route%2053-232F3E?style=flat&logo=amazon-aws&logoColor=white) ![AWS CDN](https://img.shields.io/badge/AWS%20CloudFront-232F3E?style=flat&logo=amazon-aws&logoColor=white) ![AWS ELB](https://img.shields.io/badge/AWS%20ELB-232F3E?style=flat&logo=amazon-aws&logoColor=white) |
| **Others**      | ![SSE](https://img.shields.io/badge/SSE-005571?style=flat&logo=server-sent-events&logoColor=white) ![JWT](https://img.shields.io/badge/JWT-000000?style=flat&logo=json-web-tokens&logoColor=white) ![Nginx](https://img.shields.io/badge/Nginx-009639?style=flat&logo=nginx&logoColor=white)                                                                                                                                                                                                                                                                                                                                         |
| **Environment** | ![Linux](https://img.shields.io/badge/Linux-Ubuntu-E95420?style=flat&logo=ubuntu&logoColor=white)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |

## Usage

- Login and Registration  
  <img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/sign%20in.png" alt="login-signin" width="400"/>

- View Personalized Post Recommendations  
  <img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/personal_posts.png" alt="personal-recommand" width="400"/>

- View Popular Post Recommendations  
  <img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/pop_posts.png" alt="pop-recommand" width="400"/>

- Edit Profile Page  
  <img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/member_page.png" alt="member-personal-page" width="400"/>

- View Notifications  
  <img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/notificaition.png" alt="notify" width="400"/>

## Table Schema  
<img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/db_schema.png" alt="schema" width="800"/>

## API Documentation

The APIs in this project are designed following RESTful standards.
<img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/user.png" alt="user" width="600"/>
<img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/post.png" alt="post" width="600"/>
<img src="https://github.com/WendyWang1031/threatter/blob/main/readme_images/follow.png" alt="follow" width="600"/>

## Contact

Email : w5569590@gmail.com

Linkedin : https://www.linkedin.com/in/wendywang1031/

Phone : (+886) 985-109-945

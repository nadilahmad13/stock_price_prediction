<a id="readme-top"></a>

# Stock Price Prediction - API

<!-- Header -->
<br />
<div align="center">
  <a>
    <img src="docs/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Stock Price Prediction</h3>

  <p align="center">
    Blockhouse - Backend Engineer Technical Test
    <br />
    <a href="https://www.linkedin.com/in/ahmadnadil/"><strong> Ahmad Nadil</strong></a>
    <br />
    <a href=https://github.com/nadilahmad13/stock_price_prediction><strong>GitHub Repository »</strong></a>
    <br />
    <a href="https://api.stockpriceprediction.ahmadnadil.com/"><strong>https://api.stockpriceprediction.ahmadnadil.com/</strong></a>
    <a>
  </p>
</div>

<!-- Tabel of Content -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
    </li>
    <li>
      <a href="#tech-stack">Tech Stack</a>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#installation">Installation</a></li>
        <li><a href="#how-to-run">How to Run
          <ul>
            <li><a href="#docker">Docker</a></li>
            <li><a href="#local">Local</a></li>
          </ul>
        </li>
      </ul>
    </li>
    <li><a href="#deployment">Deployment</a>
      <ul>
        <li><a href="#aws-rds">AWS RDS</a></li>
        <li><a href="#railway">Railway</a></li>
      </ul>
    </li>
    <li><a href="#api-documentation">API Documentation</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->

## About The Project

A Django-based backend system that fetches financial data from `alphavantage` public API, stores it in a relational database, implements a basic backtesting module using this historical data, and generates reports with performance results. Also integrates a simple machine learning model to predict future stock prices.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Tech Stack-->

## Tech Stack

Here are the technologies used in this project:

- [![Django][Django]][Django-url]
- [![PostgreSQL][PostgreSQL]][PostgreSQL-url]
- [![Docker][Docker]][Docker-url]
- [![AWS RDS][AWS-RDS]][AWS-RDS-url]
- [![Railway][Railway]][Railway-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- Getting Started -->

## Getting Started

Follow the instructions below to learn how to run this project.

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/nadilahmad13/stock_price_prediction
   ```
2. Change directory to the project folder
   ```sh
    cd stock_price_prediction
   ```
3. Create a `.env` file in the root directory and use the `.env.example` file as a template
   ```sh
    cp .env.example .env
   ```
4. Edit the `.env` file and fill in the required environment variables
   ```
   PGDATABASE=stock_price_prediction
       PGUSER=postgres
       PGPASSWORD=root
       PGHOST=localhost
       PGPORT=5432
       API_URL=https://www.alphavantage.co/query
       API_KEY=L8O0N4YT6W8XXB7D
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### How to Run

#### Docker

If you have Docker and Docker Compose installed, you can run the project using the following commands:

1. Build the Docker image
   ```sh
   docker-compose build
   ```
2. Run the Docker container
   ```sh
   docker-compose up
   ```
3. If you are running the project for the first time, you need to create the database schema
   ```sh
   docker-compose exec web python manage.py migrate
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

#### Local

If you want to run the project locally, you can follow the steps below:

1. Install the required Python packages
   ```sh
   pip install -r requirements.txt
   ```
2. Run the Django server
   ```sh
   python manage.py runserver
   ```
3. Create a PostgreSQL database in your local machine and don't forget to match it with the `.env` file. Below is an example of how to create a database using the `psql` command line tool:
   ```sh
   psql -U postgres
   CREATE DATABASE stock_price_prediction;
   ```
4. If you are running the project for the first time, you need to create the database schema
   ```sh
   python manage.py migrate
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Deployment

### AWS RDS

The PostgreSQL Database is deployed on AWS RDS.
Below are the steps to create a database on AWS RDS:

1. Go to the AWS Management Console and search for RDS.
2. Click on the `Create database` button.
3. Select the `Standard Create` option.
4. Choose the PostgreSQL engine.
5. Choose the version of the PostgreSQL engine.
6. Choose the free tier template.
7. Below are the examples settings that can used:

   ```
   DB instance identifier: stock-price-prediction
   Master username: postgres
   Master password: root
   DB instance size: db.t3.micro
   Storage : <leave on default settings>
   Initial database name: stock_price_prediction
   ```

8. Setup the inbound rules for the security group to allow traffic from your IP address.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

### Railway

The Django project is deployed on Railway. As the project is already dockerized, it can be easily deployed on Railway.
This project is already deployed on Railway and can be accessed using the following link: [https://api.stockpriceprediction.ahmadnadil.com/](https://api.stockpriceprediction.ahmadnadil.com/)

Below are the steps to deploy the project on Railway:

1. Create a new project.
2. Connect the project to the GitHub repository.
3. Add the environment variables in the Railway project settings.
4. Deploy the project.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## API Documentation

<!-- docs/Stock Price Prediction.postman_collection.json -->

Postman collection for the API can be found [here](docs/Stock%20Price%20Prediction.postman_collection.json)

1. GET `/api/stocks/` - Get all the stock data

   Retrieve stock data stored in the historical data table.

   Request Body:

   ```json
   {
     "symbol": "NVDA", // optional, default is all
     "count": "5" // optional, default is all
   }
   ```

2. POST `/api/stocks/` - Add a new stock data

   Fetch stock data from the `alphavantage` API and store it in the historical data table.

   Request Body:

   ```json
   {
     "symbol": "IBM",
     "outputsize": "compact" // optional, default is compact
   }
   ```

3. GET `/api/backtest/` - Get the backtest data

   Compute the simple backtesting based the historical data stored in the database and parameters provided.

   Request Body:

   ```json
   {
     "initial_investment": 1000,
     "short_ma_days": 10,
     "long_ma_days": 300,
     "symbol": "AMD"
   }
   ```

4. GET `/api/predict/` - Get the stock price prediction

   Predict the future stock price (30 days) using the machine learning model.

   The model is pre-trained using AAPL, IBM, NVDA, AMD, PFE stock data within the last 2 years.

   Request Body:

   ```json
   {
     "symbol": "AAPL"
   }
   ```

5. GET `/api/report/backtest/` - Download the backtest report

   Generate a PDF file of performance report based on the backtesting results.

   Request Body:

   ```json
   {
     "symbol": "NVDA",
     "initial_investment": 1000,
     "short_ma_days": 10,
     "long_ma_days": 300
   }
   ```

6. GET `/api/report/predict/` - Download the prediction report

   Generate a PDF file of the stock price prediction results.

   Request Body:

   ```json
   {
     "symbol": "AAPL"
   }
   ```

<p align="right">(<a href="#readme-top">back to top</a>)</p>

<!-- LINKS -->

[Django]: https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green
[Django-url]: https://www.djangoproject.com/
[PostgreSQL]: https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white
[PostgreSQL-url]: https://www.postgresql.org/
[Docker]: https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white
[Docker-url]: https://www.docker.com/
[AWS-RDS]: https://img.shields.io/badge/AWS_RDS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=orange
[AWS-RDS-url]: https://aws.amazon.com/rds/
[Railway]: https://img.shields.io/badge/Railway-24282F?style=for-the-badge&logo=railway&logoColor=white
[Railway-url]: https://railway.app/

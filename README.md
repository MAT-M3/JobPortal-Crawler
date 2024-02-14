
# ScrapyJobCrawler: Automated Job Scraping with Scrapy, Splash and Docker

## Technologies Used:

- Python
- Scrapy
- Docker
- Splash
- PostgreSQL
- Metabase
- Cron

<img src="images/dashboard.png">

## Overview:
ScrapyJobCrawler is a  scraping project designed to automate the extraction of job listings from JoDNES job portal.
**Disclaimer:** Potential future changes to the structure of the portal's website may cause the scrapy crawl to break

<img src="images/architecture.png">

## Key Features:
- **Customizable Configuration:** Users can tailor the scraping parameters to their preferences by specifying the desired position name or keyword in the **scrapy.cfg** configuration file.
<br>

- **Dynamic Scraping:** During execution, the Scrapy spider dynamically loads configuration variable (where the desired position/key word to scrape is specified), submits them to the website's search field using Splash, and scrapes the returned job offers.
<br>

- **Automated Execution:** A cron job orchestrated within the container ensures that the scraping process runs automatically when the container is launched and once a day at 10 AM UTC, providing users with up-to-date job listings.
<br>

- **Data Visualization:** Utilizing Metabase, the project offers powerful visualization capabilities, allowing users to gain insights from the scraped job data.
<br>

- **Seamless Docker Containerization:** The project is containerized using Docker, with four distinct containers (Splash, Metabase, PostgreSQL, and Python) 

## Usage:
1. Configure the `'key_word'` parameter in the **scrapy.cfg** file.
2. Run `docker compose up`
3. Go to http://localhost:3000/dashboard/1-jobs-overview to access the Metabase dashboard 

**Metabase credentials:** 
- login: user@user.com
- password: user5432







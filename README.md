# CrawlAppsInAppStore
Crawl all apps data from https://apps.apple.com by a given company name

## Problem
1. Crawl all apps data from https://apps.apple.com by a given company name.

2. The given company name format is string. 
And the application must define the definition of how to get the company name from the given string.

## Solution
1. From the given name, the application will search the company name by itunes api <[link](https://itunes.apple.com/search?media=software&entity=allArtist&attribute=softwareDeveloper&term=)> in order to get list of companies that match the given name. This itunes api will return data includes company id corresponding to the company name
2. The application will check if there is any company that match the given name by rules that defined in the application. This is how the rules work:
   1. The application will split the given name into words
   2. The application will split the company name into words
   3. The application will check if all words in the given name are in the company name
   4. By default, if the application find out more than 5 companies that match the given name, it will raise an exception: `Too many results. Please search for more specific name.`
5. After getting the company name, the application will lookup all apps of the company from develop home page https://apps.apple.com/us/developer/<company_id> and then get all apps id
6. Some cases, the company has a plenty of apps, the application will open the `See all` page from the developer home page
7. Finally, crawl all apps data by sending request to itunes lookup api https://itunes.apple.com/lookup?id= by list of ids that got from step 5 and step 6. List of ids would be split into chunks of 200 ids per request

**NOTES:** The reason I come up with this solution instead of getting directly data itunes api, 

1. itunes api does not allow to fetch more than 200 items per request and has no way to paginate the data
2. Cannot fetch enough information directly from app store websites only. So I have to combine the data from itunes api and app store websites

## Technologies
- [python-3.10](https://www.python.org/) for building backend application
- [Selenium](https://www.selenium.dev/) for crawling data
- [python-request](https://docs.python-requests.org/en/latest/) for making http request
- [Docker](https://www.docker.com/) for containerizing the application

## Installation on local machine
### Prerequisites
- [Docker](https://www.docker.com/)
- This guidance has been tested on MacOS only

### Steps
1. Open terminal and clone the project
```shell
git clone git@github.com:vanhiepdam/CrawlAppsInAppStore.git
```

2. Go to the project directory
```shell
cd CrawlAppsInAppStore
```

3. Build docker image
```shell
docker build -t app_store_crawler .
```

### Run the application
1. Run unit tests (by default, integration tests will be skipped). After running successfully, the application will print out the coverage report

```shell
docker run app_store_crawler pytest
```

2. Run integration tests

```shell
docker run app_store_crawler pytest -m integration
```

3. Run crawler with company name
    
```shell
docker run app_store_crawler python src/main.py <YOUR_COMPANY_NAME>
```

For example after running successfully, the application will print out the result like this, you can then go to the links to verify the result for each crawled company
```shell
2023-06-21 15:54:54,949 [INFO] Done. Found 69 apps.
2023-06-21 15:54:54,950 [INFO] Artist: Netflix, Inc.: 68 apps. Verify here: https://apps.apple.com/us/developer/363590054
2023-06-21 15:54:54,950 [INFO] Artist: DVD.com, A Netflix Company: 1 apps. Verify here: https://apps.apple.com/us/developer/1169772775
```

## Limitations
- The application only supports crawling data with 1 single process and 1 single thread. Web crawling is an I/O intensive task, so better to apply multi thread in order to improve the performance
- The application does not have any wait and retry mechanism. So if there is any error, the application will stop immediately
- The application does have any mechanism to change the user agent. So if the application is blocked by the website, it will stop immediately

## Improvements
To make this application in a good shape, I would improve all the limitations and also add more feature to the application:
1. Allow user to select company name from the list of companies that match the given name
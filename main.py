
from bs4 import BeautifulSoup

import requests

import time

import csv

base_url = 'https://news.ycombinator.com/news'

website_of_title = []
# Get the title of the website
for attempt in range(5):
    try:


        response = requests.get(base_url)

        soup = BeautifulSoup(response.text, 'html.parser')

        website_title = soup.title.text if soup.title else 'No Title Available'

        website_of_title.append(website_title)

        print(f"Website Title: {website_title}\n")

        break
    except (requests.ConnectionError, requests.Timeout):

        print(f"Attempt {attempt + 1} failed. Retrying The Title of the website...")

        time.sleep(5)  # Wait before retrying

ALL_information = []

All_upvote = []

max_upvote = 0

max_retries = 10

page_number = 1

while True:

    for retries in range(max_retries):

        try:

            next_url = f'{base_url}?p={page_number}'

            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'
            }

            response = requests.get(next_url, headers=headers, timeout=10)

            response.raise_for_status() # Raise an error for bad responses

            break  # Exit retry loop if successful

        except (requests.ConnectionError, requests.Timeout):

            print(f"Attempt {retries + 1} failed. Retrying...")

            time.sleep(5)  # Wait before retrying

    # if all retries reaches to its maximum retries:

    else:
        print("Max attempts reached. Exiting...")

        break  # Exit if max attempts are reached

    soup = BeautifulSoup(response.text, "html.parser")

    All_titles = soup.find_all("tr", class_="athing")

    All_points = soup.find_all("td", class_="subtext")

    for title, point in zip(All_titles, All_points):

        Rank = title.find("span", class_="rank").getText()

        Title = title.find("span", class_="titleline").a.getText()

        Url_Link = title.find("span", class_="titleline").a.get("href")

        Authors = point.find("a", class_="hnuser")

        points = point.find("span", class_="score")

        Other_Information = point.find_all("a", class_=False)

        try:
            Author = Authors.text

            points1 = points.text

            max_upvote = All_upvote[0]

            for upvote in range(len(All_upvote)):

                Upvote2 = All_upvote[upvote]

                if max_upvote < Upvote2:


                    max_upvote = Upvote2

                    print(f' this is the maximum upvote: {max_upvote}')

                    break


            Time_post = Other_Information[0].text if Other_Information else 'N/A'

            comment = Other_Information[2].text.replace('\xa0', ' ') if Other_Information else '0 comments'

        except IndexError:

            Time_post = 'N/A'

            comment = 'N/A'

            Author = 'N/A'

            points = 'N/A'

        except AttributeError:

            Time_post = 'N/A'

            comment = 'N/A'

            Author = 'N/A'

            points = 'N/A'

        print(Rank, Title, Url_Link, points, Author, Time_post, comment)

        ALL_information.append([Rank, Title, Url_Link, points, Author, Time_post, comment, max_upvote])

    page_number += 1  # Move to the next page

# Output the results
csv_file = 'hacker_news.csv'
with open(csv_file, 'w', newline='', encoding='utf-8') as file:

    writer = csv.writer(file)  # Use csv.writer for flexibility

    # Write the website title as the first row
    writer.writerow(website_of_title)

    # Write the header
    writer.writerow(['Rank', 'Title', 'Url_Link', 'Points', 'Author', 'Time_post', 'Comments', 'max_upvote'])

    # Write the data rows
    writer.writerows(ALL_information)

print(f"\nData exported to {csv_file}")

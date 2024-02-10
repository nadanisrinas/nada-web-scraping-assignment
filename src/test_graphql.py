import requests
import time
import os
from dotenv import load_dotenv
def send_graphql_request(url, query, headers=None):
    retry_attempts = 3
    for attempt in range(retry_attempts):
        response = requests.post(url, json={'query': query}, headers=headers)
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 503 and attempt < retry_attempts - 1:
            # Service Unavailable, wait before retrying
            wait_time = 2 ** attempt
            print(f"Service Unavailable, retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            # Request failed with unexpected status code, raise an exception
            response.raise_for_status()
def test_github_graphql_api_1():
    # Set the URL of the GitHub GraphQL API endpoint
    url = 'https://api.github.com/graphql'

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve GitHub personal access token from environment variable
    token = os.getenv('GITHUB_TOKEN')

    # Define the GraphQL query to retrieve information about your GitHub user
    query = """
    query {
        viewer {
            login
            name
            email
        }
    }
    """

    # Set the request headers with the GitHub personal access token
    headers = {'Authorization': f'Bearer {token}'}

    # Send the GraphQL query as a POST request to the GitHub API
    response = requests.post(url, json={'query': query}, headers=headers)

    # Check if the request was successful (status code 200)
    assert response.status_code == 200, f"Request failed with status code {response.status_code}"

    # Parse the response JSON
    data = response.json()

    # Print the response data
    print("GitHub User Information:")
    viewer = data['data']['viewer']
    print(f"Username: {viewer['login']}")
    print(f"Name: {viewer['name']}")
    print(f"Email: {viewer['email']}")

def test_github_graphql_api():
    # Set the URL of the GitHub GraphQL API endpoint
    url = 'https://api.github.com/graphql'

    # Load environment variables from .env file
    load_dotenv()

    # Retrieve GitHub personal access token from environment variable
    token = os.getenv('GITHUB_TOKEN')

    # Define the GraphQL query to retrieve information about your GitHub user
    query = """
    query {
        viewer {
            login
            name
            email
            repositories(first: 5, orderBy: {field: UPDATED_AT, direction: DESC}) {
                nodes {
                    name
                    createdAt
                    description
                }
            }
        }
    }
    """

    # Set the request headers with the GitHub personal access token
    headers = {'Authorization': f'Bearer {token}'}

    # Send the GraphQL query to the GitHub API
    data = send_graphql_request(url, query, headers=headers)

    # Print the response data
    print("GitHub User Information:")
    viewer = data['data']['viewer']
    print(f"Username: {viewer['login']}")
    print(f"Name: {viewer['name']}")
    print(f"Email: {viewer['email']}")
    print("Repositories:")
    for repo in viewer['repositories']['nodes']:
        print(f"- {repo['name']}: {repo['description']}")

if __name__ == "__main__":
    test_github_graphql_api()
    test_github_graphql_api_1()
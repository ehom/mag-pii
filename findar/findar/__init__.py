import sys
import os
from pprint import pprint as pp
import json
import argparse

from helpers.github_gql import GitHubClient as Client
from helpers.github_gql import QueryRepos, QueryMoreRepos
from helpers.github_gql import QueryProcessor

import decorators as Decorators


def main():
    def make_filename(owner):
        return "{}-repos.json".format(owner)

    owner = get_owner()

    client = Client(
        os.getenv("GITHUB_ACCESS_TOKEN")
    )

    result = get_repositories(client, owner)

    output_filename = make_filename(owner)
    save_to_files(result, output_filename)


@Decorators.timing_decorator
def get_repositories(client, owner):
    @Decorators.show_progress
    def get_next_batch(owner, cursor):
        return processor.execute(next_query, {
            'owner': owner,
            'cursor': cursor
        })

    processor = QueryProcessor(client)

    first_query = QueryRepos()
    repos = processor.execute(first_query, {
        'owner': owner,
        'firstCall': True
    })

    list_of_repos = repos['nodes']

    next_query = QueryMoreRepos()

    while repos['pageInfo']['hasNextPage']:
        repos = get_next_batch(owner, repos['pageInfo']['endCursor'])
        list_of_repos.extend(repos['nodes'])

    return list_of_repos


def get_owner():
    parser = argparse.ArgumentParser(description='list repositories')
    parser.add_argument('user_name', type=str,
                        help='GitHub user_name or org_name')
    args = parser.parse_args()

    return args.user_name


@Decorators.save_as_json_hash_table
@Decorators.save_as_json
def save_to_files(obj, filepath): pass

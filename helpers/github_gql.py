import ast
import os
import json
from pprint import pprint as pp

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

from helpers.logger import logging as Logging

# from helpers.list_repos import query_doc as query_repos
from queries.query_repos import DOCUMENT as query_repos


def GitHubClient(api_token):
    if api_token is None or len(api_token) == 0:
        raise NameError('''
        Environment variable GITHUB_ACCESS_TOKEN is not defined
        ''')

    headers = {
        'Authorization': 'token {}'.format(api_token)
    }

    _transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        use_json=True,
        headers=headers
    )

    client = Client(
        transport=_transport,
        fetch_schema_from_transport=True
    )

    return client


class QueryProcessor:
    def __init__(self, client):
        self.client = client

    def execute(self, query, query_variables):
        query_variables = json.dumps(query_variables)

        try:
            result = self.client.execute(query.document, query_variables)
            pp(result)
        except Exception as e:
            '''
            Currently, Github returns an error that is not JSON-compliant.
            A brute force string.replace() of single quotes with
            double quotes will not work since the name of the repo is
            embedded in single-quotes.

            '''

            obj = ast.literal_eval(str(e))
            raise Exception(obj['message'])

        Logging.debug("{}.{}".format(self.__class__.__name__,
                                     method_name(self.execute)))
        return query.resolve(result)


def method_name(f):
    return f.__name__


def trace_resolve(fn):
    from functools import wraps
    @wraps(fn)
    def wrapped(self, data):
        Logging.debug("{}.{}".format(self.__class__.__name__,
                                     method_name(self.resolve)))
        return fn(self, data)
    return wrapped


class QueryBase:
    def __init__(self, filename_gql):
        # query_doc = load_query_string(filename_gql)
        self.document = gql(query_repos)
        # self.document = gql(queries.query_repos.DOCUMENT)


class ResolveMixin:
    @trace_resolve
    def resolve(self, result):
        return result['repositoryOwner']['firstSet']


class ResolveNextMixin:
    @trace_resolve
    def resolve(self, result):
        return result['repositoryOwner']['nextSet']


class QueryRepos(QueryBase, ResolveMixin):
    def __init__(self):
        super().__init__('list-of-repos.gql')


class QueryMoreRepos(ResolveNextMixin, QueryRepos):
    pass


#########


class ResolveFirstSet:
    @trace_resolve
    def resolve(self, result):
        return result['repository']['firstSet']


class ResolveNextSet:
    @trace_resolve
    def resolve(self, result):
        return result['repository']['nextSet']


class QueryIssues(QueryBase, ResolveFirstSet):
    def __init__(self):
        super().__init__('get-issues.gql')


class QueryNextIssues(ResolveNextSet, QueryIssues):
    pass


class QueryProjects(QueryBase):
    def __init__(self):
        super().__init__('projects.gql')

    @trace_resolve
    def resolve(self, result):
        projects = result['repositoryOwner']['repository']['projects']['nodes']
        return [
            card
            for project in projects
            for column in project['columns']['nodes']
            for card in column['cards']['nodes']
        ]


class QueryCommits(QueryBase):
    def __init__(self):
        super().__init__('get-commits.gql')

    @trace_resolve
    def resolve(self, result):
        return result['repository']['refs']['nodes']


class QueryPullRequests(QueryBase, ResolveFirstSet):
    def __init__(self):
        super().__init__('pull-requests.gql')


class QueryNextPullRequests(ResolveNextSet, QueryPullRequests):
    pass


def load_query_string(filename):
    def locate_graphql_file(filename):
        folderpath = os.path.dirname(os.path.realpath(__file__))
        return "{}/../data/graphql/{}".format(folderpath, filename)

    filepath = locate_graphql_file(filename)
    with open(filepath) as f:
        query_string = f.read()

    return query_string

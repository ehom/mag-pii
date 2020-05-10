from collections import namedtuple

import queries.query_repos
import queries.query_projects
import queries.query_commits
import queries.query_issues

# Doing this makes the query documents Read-Only
GQL_QUERY = namedtuple('GQL_query', 'document')

query_repos = GQL_QUERY(queries.query_repos.DOCUMENT)
query_commits = GQL_QUERY(queries.query_projects.DOCUMENT)
query_issues = GQL_QUERY(queries.query_projects.DOCUMENT)
query_projects = GQL_QUERY(queries.query_projects.DOCUMENT)

DOCUMENTS = '''
query IssuesComments($repo: String!, $owner: String!, $firstCall: Boolean = false, $cursor: String = "") {
  rateLimit {
    limit
    remaining
    resetAt
  }
  repository(name: $repo, owner: $owner) {
    ...issuesFirstSet @include(if: $firstCall)
    ...issuesNextSet @skip(if: $firstCall)
  }
}

fragment issuesFirstSet on Repository {
  isPrivate
  firstSet: issues(first: 100, orderBy: {direction:DESC, field: UPDATED_AT}) {
    ...issueConnection
  }
}

fragment issuesNextSet on Repository {
  isPrivate
  nextSet: issues(first: 100, after: $cursor, orderBy: {direction:DESC, field: UPDATED_AT}) {
    ...issueConnection
  }
}

fragment issueConnection on IssueConnection {
  totalCount
  pageInfo {
    endCursor
    hasNextPage
  }
  nodes {
    title
    url
    bodyText
    updatedAt
    comments(first: 10) {
      totalCount
      nodes {
        bodyText
        url
        updatedAt
      }
    }
  }
}
'''

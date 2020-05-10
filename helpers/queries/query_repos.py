DOCUMENT = '''

query ListOfRepos($owner: String!, $firstCall: Boolean = false, $cursor: String = "") {
  rateLimit {
    limit
    remaining
    resetAt
  }
  repositoryOwner(login: $owner) {
    ...repoFieldsFirstSet @include(if: $firstCall)
    ...repoFieldsNextSet @skip(if: $firstCall)
  }
}

fragment repoFieldsFirstSet on RepositoryOwner {
  firstSet: repositories(first: 100) {
    ...repoConnection
  }
}

fragment repoFieldsNextSet on RepositoryOwner {
  nextSet: repositories(first: 100, after: $cursor) {
    ...repoConnection
  }
}

fragment repoConnection on RepositoryConnection {
  totalCount
  pageInfo {
    hasNextPage
    endCursor
  }
  nodes {
    name
    nameWithOwner
    owner {
      login
    }
    description
    isPrivate
    updatedAt
    hasIssuesEnabled
    issues {
      totalCount
    }
    projects {
      totalCount
    }
    pullRequests {
      totalCount
    }
    refs(first: 1, refPrefix: "refs/heads/") {
      totalCount
    }
  }
}

'''

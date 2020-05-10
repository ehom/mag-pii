DOCUMENT = '''
query Commits($owner: String!, $repo: String!) {
  rateLimit {
    limit
    remaining
    resetAt
  }
  repository(owner: $owner, name: $repo) {
    isPrivate
    refs(refPrefix: "refs/heads/", orderBy: {direction: DESC, field: TAG_COMMIT_DATE}, first: 100) {
      totalCount
      nodes {
        ... on Ref {
          name
          target {
            ... on Commit {
              history(first: 10) {
                nodes {
                  ... on Commit {
                    committedDate
                    message
                    url
                    comments(first: 5) {
                      totalCount
                      nodes {
                        id
                        bodyText
                        url
                        updatedAt
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
'''

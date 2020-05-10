DOCUMENT = '''

query Projects($repo: String!, $owner: String!) {
  repositoryOwner(login: $owner) {
    repository(name: $repo) {
      isPrivate
      projects(first: 100, orderBy: {direction: DESC, field: UPDATED_AT}) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          name
          body
          url
          updatedAt
          columns(first: 100) {
            totalCount
            pageInfo {
              endCursor
              hasNextPage
            }
            nodes {
              name
              url
              updatedAt
              cards {
                totalCount
                nodes {
                  note
                  updatedAt
                  url
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

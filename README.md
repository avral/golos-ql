# golos-ql
Golos blockchain GraphQL service.  

Python 3.6  
Flask  
graphene-python
golos-mongo-plugin

### Run
1. Create .env file
2. Run docker container `docker run -d -p 5000:5000 --env-file .env avral/golos-ql`
3. Complete! Use your server on http://127.0.0.1:5000/graphql

## Try: https://golos-ql.mapala.net

### Env file example
```
MONGO_HOST=
MONGO_USER=
MONGO_PASSWORD=

GOLOS_DB_NAME=
SENTRY_DSN=
```

### Example queryes
Get post with author name, balance, avatar. Comments wiht check if some user vote for this post, count of votes. Image preview. 
```
{
  post(identifier: "@avral/ru-golos-ql-anons-graphql-servera-dlya-golosa") {
    title,
    body,
    thumb,
    comments(last: 2) {
      body,
      created,
      parentAuthor,
      parentPermlink,
      author {
        name
      }
    },
    isVoted(account: "seriy"),
    netVotes,
    author {
      name,
      balanceValue,
      meta {
        profile {
          profileImage
        }
      }
    },
    votes(first: 10) {
      edges {
        node {
          voter {
            name,
          }
        }
      }
    }
  }
}
```

Get posts filtered by category and author.
GraphQL pagination standards.
```
{
  posts(author: "dark.sun", category: "mapala", first: 2, after: "6e4f5120adba2bbbac9d6d4d") {
    edges {
      node {
        title
      },
      cursor
    }
  }
}
```
Sorting - by default all edges ordered by -created.

Account:
```
{
  account(name: "avral") {
    name,
    balanceValue,
    votingPower,
    created,
    curationRewards,
    postCount,
    meta {
      profile {
        profileImage
      }
    }
  }
}
```

### Queries
```
account
post
posts
comment
comments
stats
```

For see all types/fields and queries click "< Docs" button on GraphiQl: /graphql

### Build
If you want build by your self.  
`docker build -t golos-ql .`

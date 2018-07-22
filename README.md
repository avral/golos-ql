# golos-ql
Golos blockchain GraphQL service.  

Python 3.6  
Flask  
graphene-python

### Run
1. Create .env file
2. Run docker container `docker run -d -p 5000:5000 --env-file .env avral/golos-ql`
3. Complete! Use your server on http://127.0.0.1:5000/graphql

### Env file example
```
MONGO_HOST=
MONGO_USER=
MONGO_PASSWORD=

GOLOS_DB_NAME=

PAGINATION=20
```

### Example queryes
Get post with author name, balance, avatar. Comments wiht check if some user vote for this post and count of votes. And image preview.
```
{
  post(identifier: "@avral/sumba-indonieziia-") {
    title,
    body,
    thumb,
    comments {
      body,
      created,
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
    }
  }
}
```

Get posts filtered by category and author.
```
{
  posts(author: "dark.sun", category: "mapala") {
    title
  }
}
```
Pagination - posts is divided into pages, use page param: `page=2`

### Queries
```
account
post
posts
comment
comments
stats
```

For see all types and queries click "< Docs" button on /graphql

### Build
If you want build by your self.  
`docker build -t golos-ql .`

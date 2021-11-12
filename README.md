# Django GraphQL Simple ToDo

## HOW TO RUN

just run the following instructions:

```bash
python -m venv venv
pip install -r requirements.txt
source venv/bin/activate
chmod 777 remove_migrations.sh
./remove_migrations.sh
python manage.py runserver
```

the output should be something like this:

```bash
System check identified 1 issue (0 silenced).
November 12, 2021 - 13:38:31
Django version 3.2.9, using settings 'DjangoGraphQLToDoListApplication.settings'
Starting development server at 
Quit the server with CONTROL-C.
```

## Usage

just go to `http://127.0.0.1:8000/` then,

### Test Queries and Mutations
#### fetching all users:
```json
query {
  users {
    id
    username
  }
}
```
#### create a new user:

```json
mutation {
  userCreate(username: "alice", email: "alice@gmail.com", password:"password") {
    user {
      id
      username
      email
      dateJoined
    }
  }
}
```
#### Login 

```json
mutation {
  tokenAuth(username: "your user name", password: "your password") {
    token
    payload
    refreshExpiresIn
  }
}
```
#### currentUser 

```json
query{
  currentUser{
    id
  }
}

```

#### users 

```json
query{
  users{
    id
  }
}

```

#### user Create Todo

```json
mutation {
  userCreateTodo(title: "alice") {
    todo {
      id
      title
    }
  }
}

```

#### user update Todo state

```json
mutation {
  userUpdateTodoState(id:17, state: "done") {
    todo {
      id
      title
    }
  }
}

```

#### user delete Todo

```json
mutation {
  userDeleteTodo(id:17) {
    todo {
      id
      title
    }
  }
}
```

#### Filtering
```json

query {
  todos(title_Icontains: "e", state: "in-progress") {
    edges {
      node {
        title
      }
    }
  }
}

```

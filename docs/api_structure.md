# Planned API Structure

| Route                             |        Description           |       Notes        |
|-----------------------------------|------------------------------|--------------------|
| `/`                               | Redirect to `posts/latest`   |                    |
| `/aboutme`                        | Standalone About Me Page     | Maybe not needed   |
| `/posts`                          | List all posts               |                    |
| `/posts/<int:pk>`                 | Show post by pk              | Only if published  |
| `/posts/latest`                   | Show the latest published pk |                    |
| `/author/posts`                   |                              | Protected Route    |
| `/author/posts/create`            |                              | Protected Route    |
| `/author/posts/<int:pk>/update`   |                              | Protected Route    |
| `/author/posts/<int:pk>/destroy`  |                              | Protected Route    |
| `/admin`                          | Base Django Admin Tool       |                    |

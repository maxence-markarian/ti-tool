# ti-tool

This project is a web application to help scientists in their research.

1. Install dependencies with `poetry install`
2. Synchronize database schema with `poetry run sync_db`. DANGER: will drop everything in the database
3. Start the project with `poetry run start`

Guide to use the app:

1. On the `Home` page, you can see the recent published articles, with the authors, the date, and a clickable title.

![Alt text](https://i.imgur.com/ppi3WN2.png)

2. You need to `Register` with a username and a password to use the app.

![Alt text](https://i.imgur.com/sxArDn7.png)

4. Once you are registered, you need to `Login`.

![Alt text](https://i.imgur.com/olSSE3L.png)

6. You have now two options under each article: adding the article to your favorites or sending it to another user.

![Alt text](https://i.imgur.com/gXQuKQU.png)

8. You have a `Profile` page where you can see your favorites and the articles shared with you.

![Alt text](https://i.imgur.com/GtvMxow.png)

10. You can see all the keywords the email is subscribed to on the `About` page.

![Alt text](https://i.imgur.com/DhCB4yk.png)

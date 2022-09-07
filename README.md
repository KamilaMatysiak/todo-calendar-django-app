# vTo-Do - Advanced time organizing application in Django

vTo-Do is an application created for an engineering project.  

It is an app created to help people organize their lifes with detailed to-do lists and events.
Thing that makes vTo-Do special is map module that let's you visualize all of your tasks and events on a map and send you a notification if you're nearby. Responsive design and PWA functionality let's you use the app on the phone. 

Application used to be hosted but unfortunately prices of AWS are too high for student's pocket. 

My responsibilities:
- UI/UX designer
- Frontend Developer

## Functionalities:

vTo-Do app has 4 main modules:

### 1. To-do list
- CRUD a task (name, due date and time, priority, time consumption and notes)
- set localization of a task
- choose gmail contacs (or make custom ones) 
- create categories to better organize your tasks
- assign task to other vTo-Do user

### 2. Calendar
- CRUD an event (name, date and time, notes)
- set localization of a task
- choose gmail contacs (or make custom ones) 
- set repetition of the event
- synchronize with your google calendar

### 3. Map
- see your tasks and events on the map
- see your position on the map
- get a notification if you in range of nearest task
- search for events and tasks

### 4. Account
- CRUD a account
- edit your user profile
- change your password
- sign in/sign up using your google account or vTo-Do account

### Technologies

- App was created with Django and Javascript.
- Map module was created with LeafletJS.
- Part of UI was created with Bootstrap Framework.

To get all of the django modules run:  

        pip -r requirements.txt

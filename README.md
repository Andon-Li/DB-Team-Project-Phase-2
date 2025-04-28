# DB-Team-Project-Phase-2
## Project Demonstration / Review : April 28

### Team Members:
- Andon Li
- Michael Procyk
- Astha Amin
- Ansh Patel

### Implementation Details
We chose to use Flask and SQLite for our backend.

Every page extends "base.html" using Jinja's templating feature.

## Website Outline:
Here, we run through each page url and what its purpose is.

### /base.html
- This template should be the foundation for all other pages. This contains three Jinja blocks to be extended from


### /index
- Redirect immediately to /login or /profile based on if the client has an active session.


### /login
- Present user with fields for email and password. If the email-password combination does not exist in out DB, show error message.


### /signup
- Present user with fields for all required data for the account type they wish to make.
- Verify that all user inputs are properly formatted and does not conflict with existing users.

### /profile
- Redirect immediately to the profile of the user: /profile/XXXX where XXXX is the id of the user.

### /profile/XXXX
- This is the home page of every user. Here the user can edit their information and see relevant review information.
- If the user is a seller, show an option to create a new listing.

### /edit-profile/XXXX
- Show fields for datapoints that user is allowed to change. 
- If the user is helpdesk user, allow them to change email.

### /search
- Users can search through the entire catalog by category and keyword.


### /listing/XXXX
- Show the user all datapoints of listing of id=XXXX.
- If the user is the seller of that listing, show option to edit.

### /edit-listing/XXXX
- Give user options to change all allowed datapoints.


### /cart
- Show buyer a summary of each listing in their cart including: listing price, quantity, and total cart price. 
- Allow the user to remove listings from their cart.


### /order
- Show a history of all purchases made with an option to write a review for that listing.


### /error
- Error page where message parameter will be shown to the user.

## Grading 100 pts
### Required Functionality
1. User Login - 10 pts ✅
2. Category Hierarchy - 10 pts ✅
3. Product Listing Management - 10 pts ✅
4. Order Management - 10 pts ✅
5. Product & Seller Review - 10 pts ✅
6. Product Search - 10 pts ✅
7. User Registration - 10 pts ✅
8. User Profile Update - 10 pts ✅

### Code submission - 5 pts

### Attendance to Final Submission - 5 pts

### UI Design - 10 pts

### Extra Credit
1. Shopping Cart - 5 pts ✅
2. Product Promotion - 5 pts
3. Helpdesk Support (New Category Requests) - 5 pts

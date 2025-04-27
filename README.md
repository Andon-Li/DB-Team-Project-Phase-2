# DB-Team-Project-Phase-2
## Project Demonstration / Review : April 28


## Website Outline:

### /base.html
- Header with title and buttons for search, profile, and logout.
This template should be the foundation for all other pages.
This template has 3 blocks: title, head, and body.


### /index
Redirect immediately to /login or /profile based on if the client has an active session.


### /login
- Fields for email and password.
- Button to /signup for new users.

If email and passwordHash combination does not exist in our db, display error message.


### /signup
- Fields for all required data points for a user.
- Button to /login for existing users.

Use JS to check if the password that the user wants to register follows our strength rules.

>At least 10 characters.

>At least one lowercase and one uppercase character.

>At least one special character ie:!@#$%^&*

Check if the email that the user wants to register with does not exist in our db.
If the email does not exist and the inputs follow our rules, create the account.

### /profile
Redirect immediately to the profile of the user.
/profile/XXXX where XXXX is the id of the user.

### /profile/XXXX
- Type of user (Seller, Buyer, HelpDesk)
- Ratings and reviews that they have recieved.
- If is seller profile, display link that searches for items sold by them.
- If client is at their own profile, display link to /edit-profile/XXXX.

If profile is marked as inactive/deleted, redirect to /error.


### /edit-profile/ABCD
- Fields for all data points that the user is allowed to change.
- Button at the bottom to confirm all changes.

Verify that the client either HelpDesk or is logged in as user XXXX. If that is false, redirect to /error.

Empty fields are assumed to mean "Do not change"

HelpDesk users have the unique ability to change some data points. Only show fields to change those data points to HelpDesk users.

If profile is marked as inactive/deleted, redirect to /error.


### /search
- Four fields for search criteria: Listing Title, Seller, Category, Minimum Rating.

These are AND criteria. Only show listings that satisfy all criteria.
Require the user to fill out at least one criteria

### /search?term=ABCD&seller=ABCD&category=ABCD&rating=1.23
- 


### /listing/XXXX
- Title of listing
- Seller
- Price
- Qty available
- Seller rating
- Listing rating and reviews

If listing is inactive, redirect to /error


### /edit-listing/XXXX
- 



### /cart
- Display each item user has put in cart with price, qty, seller info.
- Each item will have a delete button.
- Checkout button 

Buyer only. If user is not 


### /checkout
- Condensed summary of cart.
- Total price of cart
- Address and financial info of user.

Buyer only.


### /error
message parameter will be shown to the user.

## Required Functionalities

### User Login
/login /logout
Users who are logged in are tracked using Flask sessions.


### Category Hierarchy
Each listing belongs to a node.
Each node has a parent.
The top level node is "root" and does not have a parent.


### Product Listing Management
/edit-listing/XXXX


### Order Management
This rolls into our shopping cart functionality


### Product & Seller Review



### Product Search
/search
Users can search for listings by Title, Seller, Category, and Rating.


### User Registration
/signup


### User Profile Update
/edit-profile/XXXX


## Grading 100 pts
### Required Functionality
1. User Login - 10 pts ✅
2. Category Hierarchy - 10 pts ✅
3. Product Listing Management - 10 pts
4. Order Management - 10 pts
5. Product & Seller Review - 10 pts
6. Product Search - 10 pts ✅
7. User Registration - 10 pts ✅
8. User Profile Update - 10 pts

### Code submission - 5 pts

### Attendance to Final Submission - 5 pts

### UI Design - 10 pts

### Extra Credit
1. Shopping Cart - 5 pts
2. Product Promotion - 5 pts
3. Helpdesk Support (New Category Requests) - 5 pts

# DB-Team-Project-Phase-2
## Project Demonstration / Review : April 28-29 *Tentative*

## Website Outline:
### /index
Redirect immediately to /login or /profile/XXXX based on if the client has an active session.


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


### /profile/XXXX
- Type of user (Seller, Buyer, HelpDesk)
- Ratings and reviews that they have recieved.
- If is seller profile, display link that searches for items sold by them.
- If client is at their own profile, display link to /edit-profile/XXXX.

If profile is marked as unactive/deleted, redirect to /error.


### /edit-profile/ABCD
- Fields for all data points that the user is allowed to change.
- Button at the bottom to confirm all changes.

Verify that the client either HelpDesk or is logged in as user XXXX. If that is false, redirect to /error.

Empty fields are assumed to mean "Do not change"

HelpDesk users have the unique ability to change some data points. Only show fields to change those data points to HelpDesk users.

If profile is marked as unactive/deleted, redirect to /error.


### /search
- Four fields for search criteria: Listing Title, Seller, Category, Minimum Rating.

These are AND criteria. Only show listings that satisfy all criteria.


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




# CSCA20 Project Report

## Team

--------

**Team Member A**  
First Name: Joe  
Last Name: Armitage  
Student Number: 999030141  
UofT E-mail Address: joe.armitage@mail.utoronto.ca  

**Team Member B**  
First Name: Angela  
Last Name: Zavaleta-Bernuy  
Student Number: 1000000001  
UofT E-mail Address: angela.zavaletabernuy@mail.utoronto.ca  

**Team Member C (Optional)**  
First Name: Brian  
Last Name: Harrington  
Student Number: 7  
UofT E-mail Address: brian.harrington@utsc.utoronto.ca

## Project Plan

--------

### Project Title: Store

### Description

We will extend the lab8 code to provide a fully functional store interactive store simulation using
the Python command-line text interface. Our final project will give users the abilities to:

- Log in (username and password)
- Start a shopping session (with an empty cart)
- Show all items in the store
- Search for products of a certain colour, or with a given name
- Add those products to a shopping cart if there is sufficient inventory
- Attempt checkout by:
  - Purchasing those products, if they have enough money
  - Or rejecting the purchase, otherwise
- Then, update the user's amount of money (wallet), if needed

### Week 1 Plan

**Before** the first tutorial will have:

- A function for printing the whole CSV file as a pretty table
- A function for building a shopping list
- 2 functions for:
  - Searching by colour
  - Searching by price

**After** the first tutorial will have:

- A function to check if a shopping list is affordable, given a budget
- An interactive interface for logging in and looking at the store

What is your backup plan if things don’t work out as planned?

- Just add functions to the store program that may help someone else finish this cool store another day.

## Weekly Reports

-----------------

### Week 1 Report

Though we had planned to add the interactive interface before this tutorial was over, we found that
the logic for checking if an item is affordable is difficult and required the attention of two of
our team members for the whole period. The other team member was able to confer with the TA and 
debug both the shopping_list and pint_csv functions.

Though we were quite productive, we are behind our targets. We will add as many features as we can,
but it seems we must resort to our backup now.

### Week 2 Report

We managed to squeeze in some 2 extra functions which:

- Give all available colours of an item
- Display which items have less than a certain number (MIN_STOCK) available

Since our tutorial is on Monday, we had no extra time to work.

## References

-------------

We shamelessly copied the starter code from lab8, found at:
https://uoft.me/a20-lab8

- Lines 0 - 125 are *not* our work.
- Lines 128 - 197 were implemented by us, but designed by CSCA20's lab8 creator.

## Repo & Video

---------------

Our Python code is uploaded to:
https://github.com/angelazb/CSCA20F19/blob/master/store/store.py

And out video is at:
https://www.youtube.com/watch?v=oHg5SJYRHA0

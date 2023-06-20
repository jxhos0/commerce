# CS50w Project 2 - Commerce

This is my submission for the CS50w Commerce project

## Overview

Creating an e-commerce website, inspiration was drawn from both eBay and Amazon to try provide an intuitive user friendly experience.

Users are able to view create listings, comment and bid on listings as well as view listings on the platforms. Users are able to filter listings based on active status, category and by if the listing is theirs or they have won the listing.

Viewing a page of listings, they are listed in descending order based on time remaining, with listing overviews showing:

- Title
- Description
- Photo
- Current price
- Number of bids
- Time remaining
- Seller

## The Design

### Back-End

Django was implemented for the backend design of this website and the templates funtionality and custom template tags features were heavily relied on to create each HTML page. Information regarding items and their relative data was passed in for rendering by Django, while simultaneously performing database checks on price, time remaining, comments and watchlists.

### Front-End

HTML and CSS was used for the front-end design of this website, making use of grid for various elements in the website including the listing cards.

## Testing the Site

If you want to test the site yourself, the login form is alread prefilled out with a test account login details.

Should the form not be pre-populated use the following information:

User: test_account
Password: test_account

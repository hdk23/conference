# README for DALI API CHALLENGE
For the DALI API Challenge, I integrated two APIs:
1. Google Calendar
2. Stripe

> Note: the web app only runs on localhost. This is also my first time ever using APIs,
> so I have only been able to implement only some basic features of the APIs.
> I completed the API Challenge on top of one of my side projects.
> The commit hash that begins my API challenge is f0d127f.

The use of each API is detailed below.

To test the website, here is the login info for a staff account and a superuser account:
### Staff Account
- Username: dalistaff
- Password: dali2021

### Superuser Account
- Username: dalisuperuser
- Password: dali2021

## Google Calendar API
Once logged in to either account, you will see a button that says "Add Calendar Entries."
Once the user clicks on this button, if the user is logged into their Google Account,
the calendar entries for each conference session will automatically be added to their Google Calendar.

## Stripe API
Because I built this web app independently, I had limited funds to work with.
By receiving some donations from users that are satisfied with the service,
I will be able to use those funds for scaling up and building my server.
Once I generate enough funds, I will be able to deploy it on a web service.

If the user clicks on the button that says "Click Here to Make Your Contribution,"
they will be directed to a checkout page that allows the user to choose an amount to donate
and enter their credit card information. Once they click on "Contribute Now," their payment will be processed.
An alert thanks the user for their contribution.
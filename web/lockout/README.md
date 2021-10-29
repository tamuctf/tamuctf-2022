# Lock Out

## Description

I seem to have locked myself out of my admin panel! Can you find a way back in for me?

## Solution

The attack target is the login page. I first tried to login with just the normal admin admin credentials and it looked like the entire page simply refreshed. I opened the page in proxy and was able to notice that the login request was a POST request made to `admin.php`. If I tried to simply access `admin.php`, I would get immediately redirected back to `login.php.` However, if I look at the HTTP history, I could render the responses of the POST request to`admin.php` and see that the page before I was redirected away had a button to display the flag. I inspected the HTML and replicated the GET request that the button would do to then again, find the `admin.php` page with the flag displayed in the HTTP history. 

`gigem{if_i_cant_wear_croc_martins_to_industry_night_then_im_not_going}`

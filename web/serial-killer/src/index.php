<?php
include_once 'GetPage.php';

if(empty($_COOKIE['PHPSESSID']))
{
    $page = new GetPage;
    $page->file = "index.html";

    setcookie(
        'PHPSESSID',
        base64_encode(serialize($page)),
        time()+60*60*24,
        '/'
    );
}

$cookie = base64_decode($_COOKIE['PHPSESSID']);
unserialize($cookie);
?>
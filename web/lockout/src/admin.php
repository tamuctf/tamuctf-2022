<?php
    header("Location: login.php");

    if(isset($_GET['PrintFlag'])) {
	printflag();
    }

    function printflag() {
	echo "<p>gigem{if_i_cant_wear_croc_martins_to_industry_night_then_im_not_going}</p>";
    }
?>

<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="/static/admin.css">
</head>
<body>
    <h1>Industry Night Shopping List</h1>
    <p>Croc Martins</p>
    <img src="static/crocmartins.jpg" alt="Croc-Martins">
    <form action="admin.php" method="get">
	<input type="submit" name="PrintFlag" value="PrintFlag">
    </form>
</body>

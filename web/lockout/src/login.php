<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="/static/login.css">
</head>
<body>
<form action="admin.php" method="post">
    <div class="container">
        <label for="uname"><b>Username</b></label>
        <input type="text" placeholder="Enter Username" name="username" required>

        <label for="psw"><b>Password</b></label><br>
        <input type="password" placeholder="Enter Password" name="password" required>

        <button type="submit">Login</button>
    </div>
</form>
</body>

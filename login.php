<?php
session_start();

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST["username"];
    $password = $_POST["password"];

    // เช็ค username และ password (ใส่ข้อมูลจริงของแอดมินตรงนี้)
    if ($username === "admin" && $password === "3770") {
        $_SESSION["logged_in"] = true;
        header("Location: index.html");
        exit;
    } else {
        echo "Invalid username or password";
    }
}
?>

<form method="POST" action="login.php">
    <input type="text" name="username" placeholder="Username" required><br>
    <input type="password" name="password" placeholder="Password" required><br>
    <button type="submit">Login</button>
</form>

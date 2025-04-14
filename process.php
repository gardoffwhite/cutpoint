<?php
session_start();
if (!isset($_SESSION["logged_in"])) {
    header("Location: login.php");
    exit;
}

$charname = $_POST["charname"];
$str = $_POST["str"];
$dex = $_POST["dex"];
$int = $_POST["int"];
$money = $_POST["money"];

$login_url = "http://nage-warzone.com/admin/index.php";
$edit_url = "http://nage-warzone.com/admin/charedit.php";

// รหัสผ่านแอดมิน (ใส่ของจริงตรงนี้)
$admin_user = "admin";
$admin_pass = "your_password_here";

// เริ่ม cURL
$ch = curl_init();

// Login ก่อน
curl_setopt($ch, CURLOPT_URL, $login_url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, "username=$admin_user&password=$admin_pass&submit=Submit");
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_COOKIEJAR, "cookie.txt");
curl_setopt($ch, CURLOPT_COOKIEFILE, "cookie.txt");
curl_exec($ch);

// Step 1: กรอกชื่อตัวละคร
curl_setopt($ch, CURLOPT_URL, $edit_url);
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, "charname=$charname&searchname=Submit");
curl_exec($ch);

// Step 2: ส่งค่าแก้ไข
$postData = http_build_query([
    "lv" => "",
    "exp" => "",
    "eclv" => "",
    "ecexp" => "",
    "str" => $str,
    "dex" => $dex,
    "int" => $int,
    "money" => $money,
    "lvpoint" => "",
    "skpoint" => "",
    "esp" => "",
    "lic" => "",
    "spt" => "",
    "bankmoney" => "",
    "cmap" => "",
    "hero" => "",
    "x" => "",
    "y" => "",
    "z" => "",
    "update" => "Update"
]);

curl_setopt($ch, CURLOPT_URL, $edit_url . "?charname=" . urlencode($charname));
curl_setopt($ch, CURLOPT_POST, 1);
curl_setopt($ch, CURLOPT_POSTFIELDS, $postData);
$response = curl_exec($ch);

curl_close($ch);

echo "อัปเดตข้อมูลสำเร็จ!";
?>

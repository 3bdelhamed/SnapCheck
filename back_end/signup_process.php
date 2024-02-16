<?php
define("localhost", "localhost");
define("password", "");
define("username", "root");
define("dbname", "university");

@$conn = mysqli_connect(localhost, username, password, dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $name = $_POST["name"];
    $id = strtolower(str_replace(" ", "_", $name));

    $checkQuery = "SELECT id FROM student WHERE id = '$id'";
    $result = $conn->query($checkQuery);

    if ($result->num_rows > 0) {
        $id = $id . '_' . time();
    }

    $targetDir = "uploads/";
    $targetFile = $targetDir . basename($_FILES["image"]["name"]);
    $imageFileType = strtolower(pathinfo($targetFile, PATHINFO_EXTENSION));

    $allowedFormats = array("jpg", "jpeg", "png");

    if (in_array($imageFileType, $allowedFormats)) {
        move_uploaded_file($_FILES["image"]["tmp_name"], $targetFile);

        $sql = "INSERT INTO student (name, image) VALUES ('$name', '$targetFile')";

        if ($conn->query($sql) === TRUE) {
            echo "Signup successful!";
        } else {
            echo "Error: " . $sql . "<br>" . $conn->error;
        }
    } else {
        echo "Invalid image format. Allowed formats: JPG, JPEG, PNG.";
    }
}

$conn->close();

<?php
// connect db
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

    $sql = "INSERT INTO student (name) VALUES ('$name')";

    if ($conn->query($sql) === TRUE) {
        // Retrieve the last inserted ID
        $id = $conn->insert_id;

        $targetDir = "uploads/";
        $imageFileType = strtolower(pathinfo($_FILES["image"]["name"], PATHINFO_EXTENSION));
        $targetFile = $targetDir . $id . "." . $imageFileType;

        $allowedFormats = array("jpg", "jpeg", "png");

        if (in_array($imageFileType, $allowedFormats)) {
            move_uploaded_file($_FILES["image"]["tmp_name"], $targetFile);

            // Update the record with the correct image filename
            $updateSql = "UPDATE student SET image = '$targetFile' WHERE id = $id";

            if ($conn->query($updateSql) === TRUE) {
                echo "Signup successful!";
            } else {
                echo "Error updating record: " . $conn->error;
            }
        } else {
            echo "Invalid image format. Allowed formats: JPG, JPEG, PNG.";
        }
    } else {
        echo "Error: " . $sql . "<br>" . $conn->error;
    }
}

$conn->close();
?>

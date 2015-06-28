<?php
    print_r($_POST);
    
    $uploaddir = './output/';
    $file = basename($_FILES['userfile']['name']);
    $uploadfile = $uploaddir . $file;
    
    if (move_uploaded_file($_FILES['userfile']['tmp_name'], $uploadfile)) {
        echo "SUCCESS!";
    }
    
?>
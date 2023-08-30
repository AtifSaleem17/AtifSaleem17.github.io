<?php
    if(isset($_REQUEST['email'])){
        //get data from form 
        $name = $_REQUEST['name'];
        $email= $_REQUEST['email'];
        $message= $_REQUEST['message'];
        $mobile= $_REQUEST['phone'];

        $to = "arsenkarselyan@gmail.com";
        $subject = "Cavalli Residences";
        $txt ="Name = ". $name . "\r\n Email = " . $email . "\r\n Message =" . $message ."\r\n Phone Number=" . $mobile;
        $headers = "From:info@homes-dxb.com" . "\r\n" .
        "CC:rafirao52@gmail.com";
        if($email!=NULL){
            @mail($to,$subject,$txt,$headers);
            header("Location: thankyou.php");
            exit;
        }
        //redirect
        header("Location: index.php");
    }
?>
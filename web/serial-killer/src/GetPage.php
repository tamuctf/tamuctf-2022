<?php
class GetPage {
    public $file;

    public function __destruct() {
        $filter = "../";
        if(strpos($this->file, $filter) !== false) {
            echo '<div class="container"><h1>You should not be doing that</h1></div>';
            include("/var/www/html/index.html");
        } else {
            $this->file = urldecode($this->file);
            include("/var/www/html/{$this->file}");
        }
    }
}
?>

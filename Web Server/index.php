<html>
<head>
<link rel="stylesheet" type="text/css" href="main.css">
 <script src="//ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js"></script>
<script src="scripts.js">
</script>
<script type="text/javascript">

function stopRKey(evt) {
  var evt = (evt) ? evt : ((event) ? event : null);
  var node = (evt.target) ? evt.target : ((evt.srcElement) ? evt.srcElement : null);
  if ((evt.keyCode == 13) && (node.type=="text"))  {return false;}
}

document.onkeypress = stopRKey;

</script>
</head>
  <body>
<script>
  (function(i,s,o,g,r,a,m){i['GoogleAnalyticsObject']=r;i[r]=i[r]||function(){
  (i[r].q=i[r].q||[]).push(arguments)},i[r].l=1*new Date();a=s.createElement(o),
  m=s.getElementsByTagName(o)[0];a.async=1;a.src=g;m.parentNode.insertBefore(a,m)
  })(window,document,'script','//www.google-analytics.com/analytics.js','ga');

  ga('create', 'UA-43684054-3', 'auto');
  ga('send', 'pageview');
</script>
    <div>
      Give me a Command!
      <form action="demo_form.asp">
        <input type="text" name="fname" autofocus><br>
      </form>
    </div>

    <div>
      <table>
        <tr>
          <td>
            tell the bot to go "around the box"
          </td>
          <td>
            tell the bot to "follow" a color
          </td>
          <td>
            tell the bot to "play mario song"
          </td>
        </tr>
      </table>
    </div>
  </body>
</html>

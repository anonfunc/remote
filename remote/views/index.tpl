<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="/bower_components/bootstrap-css/css/bootstrap.min.css" media="all">
    <title>Remote</title>
  </head>
  <body>
    <div class="container">
      <div class="row">
        <div class="span2">
        Roku
        </div>
        <div class="span10">
        <table class="table">
          <tr>
            <td><a action="/roku/press/Back">Back</a></td>
            <td><a action="/roku/press/Up">Up</a></td>
            <td><a action="/roku/press/Home">Home</a></td>
          </tr>
          <tr>
            <td><a action="/roku/press/Left">Left</a></td>
            <td><a action="/roku/press/Select">Select</a></td>
            <td><a action="/roku/press/Right">Right</a></td>
          </tr>
          <tr>
            <td></td>
            <td><a action="/roku/press/Down">Down</a></td>
            <td></td>
          </tr>
        </table>
        </div>
      </div>
    </div>
    <script src="/bower_components/jquery/jquery.min.js"></script>
    <script src="/bower_components/bootstrap-css/js/bootstrap.min.js"></script>
    <script src="/static/js/remote.js"></script>
  </body>
</html>

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <title>ReCLIne</title>
    <meta name="description" content="Web Apps from CLI scripts.">
    <meta name="author" content="@alixedi">
  </head>
  <body>
    <div class="container">
      <h1>{{ self.get_title() }}</h1>
      % for argparser in self.get_argparsers():
        {{ !self.render_argparser(argparser) }}
    </div>      
  </body>
</html>

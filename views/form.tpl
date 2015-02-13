<p>{{ !self.get_description() }}</p>
<form method="POST" action="." enctype="multipart/form-data">
  % for group in self.get_groups():
    {{ !self.render_group(group) }}
  % end
  <input type=submit value="Go" />
</form>
<p>{{ !self.get_epilog() }}</p>